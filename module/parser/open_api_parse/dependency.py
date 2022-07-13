import nltk
import copy
from typing import Union
from log.get_logging import Log
from fuzzywuzzy import fuzz
from anytree import NodeMixin, RenderTree
from foREST_setting import foRESTSettings
from entity.resource_pool import resource_pool
from entity.api_info import *
from module.utils.utils import *
from module.foREST_monitor.foREST_monitor import Monitor


def smart_match(name_1, parent_name_1, type_1, name_2, parent_name_2, type_2, base_match_point=60) -> int:
    """ Compare two fields similarity"""
    if name_1 is None or name_2 is None:
        return 0
    match_point = max(fuzz.partial_ratio(parent_name_1 + name_1,
                                         parent_name_2 + name_2),
                      fuzz.partial_ratio(name_2, name_1))
    if type_1 != type_2:
        match_point -= 100 - base_match_point
    if match_point > base_match_point:
        return (match_point - base_match_point) / (100 - base_match_point)
    else:
        return 0


class SetKeyValueDependency:
    """
        find the parameter dependency and save it in field_info.depend_list
    """

    def __init__(self, api_info_list):
        self.api_info_list = api_info_list  # type: Monitor().api_list
        self.api_numbers = len(api_info_list)
        self.current_field_info = None  # type: Union[FieldInfo, None]
        self.current_api_info = None  # type: Union[APIInfo, None]
        self.current_parent_resource_name = ''
        self.current_compare_field_info = None
        self.current_compare_api_info = None
        self.not_reference_field = []
        self.key_depend_api_list = []
        self.depended_field_list = []
        self.depended_field_path = []

    def find_depend_API(self):
        for api_info in self.api_info_list:
            self.current_compare_api_info = api_info
            self.depended_field_list = []
            if not api_info.resp_param or api_info == self.current_api_info:
                continue
            for field_info in api_info.resp_param:
                self.current_compare_field_info = field_info
                self.depended_field_path = [api_info.api_id]
                parent_resource_name = resource_pool().find_parent_resource_name(api_info.path)
                if self.find_depend_field(field_info, parent_resource_name) and \
                        self.current_field_info.require and \
                        api_info.api_id not in self.key_depend_api_list:
                    self.key_depend_api_list.append(api_info.api_id)

    def find_depend_field(self, compare_field, parent_name=''):
        if parent_name is None:
            parent_name = ''
        self.depended_field_path.append(compare_field.field_name)
        real_field_name, real_compare_field_name = None, None
        if Monitor().annotation_table:
            real_field_name = annotation_key_table_parse(Monitor().annotation_table,
                                                         self.current_api_info.path,
                                                         self.current_api_info.http_method,
                                                         self.current_field_info.field_name,
                                                         self.current_field_info.location)
        if Monitor().annotation_key_table:
            real_compare_field_name = annotation_key_table_parse(Monitor().annotation_key_table,
                                                                 self.current_compare_api_info.path,
                                                                 self.current_compare_api_info.http_method,
                                                                 self.current_compare_field_info.field_name,
                                                                 self.current_compare_field_info.location)
        if not real_field_name:
            real_field_name = self.current_field_info.field_name
        if not real_compare_field_name:
            real_compare_field_name = compare_field.field_name
        point = smart_match(real_field_name, self.current_parent_resource_name,
                            self.current_field_info.field_type, real_compare_field_name,
                            parent_name, compare_field.field_type, foRESTSettings().similarity_cardinality)
        if point:
            depend_point = self.current_field_info.get_depend(self.depended_field_path[0], self.depended_field_path[1:])
            if depend_point:
                depend_point.base_score = point
            else:
                depend_point = DependPoint(self.api_info_list[self.depended_field_path[0]], self.depended_field_path[1:],
                                       point)
                self.current_field_info.depend_list.append(depend_point)
            self.depended_field_path.pop(-1)
            return True
        elif compare_field.field_type == 'dict':
            if compare_field.object:
                for object_info in compare_field.object:
                    if object_info.field_name:
                        if self.find_depend_field(object_info, compare_field.field_name):
                            self.depended_field_path.pop(-1)
                            return True
        elif compare_field.field_type == 'list':
            if self.find_depend_field(compare_field.array, compare_field.field_name):
                self.depended_field_path.pop(-1)
                return True
        self.depended_field_path.pop(-1)
        return False

    def get_field_dependency(self, field_info: FieldInfo):
        self.current_field_info = field_info
        if field_info.field_name:
            self.find_depend_API()
        if not field_info.depend_list:
            if field_info.field_name not in self.not_reference_field:
                self.not_reference_field.append(field_info.field_name)
        if field_info.field_type == 'list':
            self.get_field_dependency(field_info.array)
        if field_info.field_type == 'dict':
            if field_info.object:
                for object_info in field_info.object:
                    self.get_field_dependency(object_info)

    def get_dependency(self):
        """get every field dependency reference"""
        for api_info in self.api_info_list:
            self.current_api_info = api_info
            self.current_parent_resource_name = resource_pool().find_parent_resource_name(api_info.path)
            self.key_depend_api_list = []
            if api_info.req_param:
                # traverse every parameter
                for req_field_info in api_info.req_param:
                    if req_field_info.field_type == 'bool':
                        continue
                    self.get_field_dependency(req_field_info)
            api_info.key_depend_api_list = self.key_depend_api_list
        log = Log("no_reference_key.json")
        log.save_json(self.not_reference_field)
        return self.api_info_list


sno = nltk.stem.SnowballStemmer('english')


class SemanticNode(NodeMixin):

    def __init__(self, name, parent=None, children=None):
        super(SemanticNode, self).__init__()
        self.name = name
        self.resource = []
        self.method_dic = {}
        self.parent = parent
        if children:
            self.children = children


class SemanticTree:

    def __init__(self, api_list):
        self.api_list = api_list
        self._root = SemanticNode('root')
        self.create_tree()

    def create_tree(self):
        for api_info in self.api_list:
            self.find_node(api_info.path.split('/')[1:], api_info.http_method, api_info.api_id, self._root)
        # for pre, fill, node in RenderTree(self._root):   print tree
        #     treestr = u"%s%s" % (pre, node.name)
        #     print(treestr.ljust(8), node.method_dic)
        self.add_close_api(self._root)

    @property
    def root(self):
        return self._root

    def add_close_api(self, node):
        close_api_list = []
        if node.method_dic:
            if node.ancestors:
                for ancestors_node in node.ancestors:
                    close_api_list += self.add_close_node_api(ancestors_node)
            close_api_list += self.add_close_node_api(node)
            if node.parent and node.parent.children:
                for parent_children_node in node.parent.children:
                    close_api_list += self.add_close_node_api(parent_children_node)
            for method in node.method_dic:
                self.api_list[node.method_dic[method]].close_api += close_api_list
        if node.children:
            for children_node in node.children:
                self.add_close_api(children_node)

    @staticmethod
    def add_close_node_api(node):
        close_api = []
        if node.method_dic:
            for method in node.method_dic:
                close_api.append(node.method_dic[method])
        return close_api

    @staticmethod
    def find_node(api_path_nodes, api_method, api_id, parent_node):
        if not api_path_nodes:
            if api_method == 'post' and not is_path_variable(parent_node.name):
                resource_pool().resource_name_dict[sno.stem(parent_node.name)] = []
            parent_node.method_dic[api_method] = api_id
            return
        flag = 0
        if parent_node.children:
            for child in parent_node.children:
                if child.name == api_path_nodes[0]:
                    flag = 1
                    child_node = child
                    break
        if flag == 0:
            child_node = SemanticNode(api_path_nodes[0], parent=parent_node)
        SemanticTree.find_node(api_path_nodes[1:], api_method, api_id, child_node)
