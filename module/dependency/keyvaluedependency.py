import nltk
import copy
from entity.resource_pool import foREST_POST_resource_pool
from fuzzywuzzy import fuzz
from module.utils.string_march import StringMatch


def Dependency(open_api_list):
    semantic_tree = CreateSemanticTree(open_api_list)
    tree_root = semantic_tree.create_tree
    key_value_parser = SetKeyValueDependency(open_api_list)
    key_value_parser.get_dependency()
    return tree_root

class SetKeyValueDependency:
    """
        find the parameter dependency and save it in field_info.depend_list
    """

    def __init__(self, api_info_list):
        self.api_info_list = api_info_list
        self.api_numbers = len(api_info_list)
        self.current_field_info = None
        self.current_api_info = None
        self.current_parent_resource_name = None
        self.current_compare_field_info = None
        self.current_compare_api_info = None
        self.not_reference_field = []
        self.key_depend_api_list = []
        self.depended_field_list = []
        self.depended_field_path = []

    def find_depend_API(self):
        depend_field_dict = {}
        for api_info in self.api_info_list:
            self.current_compare_api_info = api_info
            self.depended_field_list = []
            if not api_info.resp_param or api_info.http_method != 'post':
                continue
            for field_info in api_info.resp_param:
                self.current_compare_field_info = field_info
                self.depended_field_path = [api_info.api_id]
                parent_resource_name = foREST_POST_resource_pool.find_parent_resource_name(api_info.path)
                if self.find_depend_field(field_info, parent_resource_name) and \
                        self.current_field_info.require and \
                        api_info.api_id not in self.key_depend_api_list:
                    self.key_depend_api_list.append(api_info.api_id)

    def find_depend_field(self, compare_field, parent_name=''):
        if parent_name is None:
            parent_name = ''
        self.depended_field_path.append(compare_field.field_name)
        real_field_name = StringMatch.get_real_name_from_external(self.current_api_info.path,
                                                                  self.current_api_info.http_method,
                                                                  self.current_field_info.field_name,
                                                                  self.current_field_info.location)
        real_compare_field_name = StringMatch.get_real_name_from_external(self.current_compare_api_info.path,
                                                                          self.current_compare_api_info.http_method,
                                                                          self.current_compare_field_info.field_name,
                                                                          self.current_compare_field_info.location)
        if not real_field_name:
            real_field_name = self.current_field_info.field_name
        if not real_compare_field_name:
            real_compare_field_name = self.current_compare_field_info.field_name
        compare_method = Compare(real_field_name, self.current_parent_resource_name,
                                 self.current_field_info.field_type, real_compare_field_name,
                                 parent_name, compare_field.field_type)
        point = compare_method.smart_match()
        if point:
            self.current_field_info.depend_list[0].append(copy.deepcopy(self.depended_field_path))
            self.current_field_info.depend_list[1].extend([point, point])
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

    def get_field_dependency(self, field_info):
        self.current_field_info = field_info
        if field_info.field_name:
            self.find_depend_API()
        if not field_info.depend_list[0]:
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
            self.current_parent_resource_name = foREST_POST_resource_pool.find_parent_resource_name(api_info.path)
            self.key_depend_api_list = []
            if api_info.req_param:
                # traverse every parameter
                for req_field_info in api_info.req_param:
                    if req_field_info.field_type == 'bool':
                        continue
                    self.get_field_dependency(req_field_info)
            api_info.key_depend_api_list = self.key_depend_api_list
        Tool.save_no_reference(self.not_reference_field)
        return self.api_info_list


class Compare:

    def __init__(self, compare_field_name, compare_parent_resource_name, compare_field_type, compared_field_name,
                 compared_parent_resource_name, compared_field_type):
        self.compare_field_name = compare_field_name
        self.compare_parent_resource_name = compare_parent_resource_name
        self.compare_field_type = compare_field_type
        self.compared_field_name = compared_field_name
        self.compared_field_type = compared_field_type
        self.compared_parent_resource_name = compared_parent_resource_name

    def simple_match(self):
        if self.compared_field_name is None:
            return None
        self.compared_field_name.lower()
        self.compare_field_name.lower()
        if self.compared_field_name == self.compare_field_name and self.compared_field_type == self.compare_field_name:
            return self.compared_field_name
        else:
            return None

    def smart_match(self):
        if self.compared_field_name is None:
            return 0
        match_point = max(fuzz.partial_ratio(self.compare_parent_resource_name + self.compare_field_name,
                                             self.compared_parent_resource_name + self.compared_field_name),
                          fuzz.partial_ratio(self.compare_field_name, self.compared_field_name))
        if self.compare_field_type != self.compared_field_type:
            match_point -= 30
        if match_point > 70:
            return (match_point-70)/3
        else:
            return 0


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


class CreateSemanticTree:

    def __init__(self, api_list):
        self.api_list = api_list
        self.root = SemanticNode('root')

    @property
    def create_tree(self):
        for api_info in self.api_list:
            self.find_node(api_info.path.split('/'), api_info.http_method, api_info.api_id, self.root)
        for pre, fill, node in RenderTree(self.root):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), node.method_dic)
        self.add_close_api(self.root)
        return self.root

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
            if api_method == 'post' and not StringMatch.is_path_variable(parent_node.name):
                foREST_POST_resource_pool.resource_name_dict[sno.stem(parent_node.name)] = []
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
        CreateSemanticTree.find_node(api_path_nodes[1:], api_method, api_id, child_node)