import json
import random
from typing import List


class JsonHandle:
    """Basic tool class for processing json objects"""

    @staticmethod
    def dic2json(api_parameters_dic):
        return json.dumps(api_parameters_dic)

    @staticmethod
    def json2dic(json_string):
        return json.loads(json_string)

    @staticmethod
    def is_json(dic):
        try:
            return json.loads(dic)
        except:
            return False


def iter_node(rows, road_step, target, mode):
    """Take path from the dictionary based on the target value"""
    if isinstance(rows, dict):
        key_value_iter = (x for x in rows.items())
    elif isinstance(rows, list):
        key_value_iter = (x for x in enumerate(rows))
    else:
        return
    for key, value in key_value_iter:
        current_path = road_step.copy()
        current_path.append(key)
        if mode == 'key':
            check = key
        else:
            check = value
        if check == target:
            yield current_path
        if isinstance(value, (dict, list)):
            yield from iter_node(value, current_path, target, mode)


class izipDestinationMatching(object):
    __slots__ = ("attr", "value", "index")

    def __init__(self, attr, value, index):
        self.attr, self.value, self.index = attr, value, index

    def __repr__(self):
        return "izip_destination_matching: found match by '%s' = '%s' @ %d" % (self.attr, self.value, self.index)


def izip_destination(a, b, attrs, addMarker=True):
    """
    Returns zipped lists, but final size is equal to b with (if shorter) a padded with nulls
    Additionally also tries to find item reallocations by searching child dicts (if they are dicts) for attribute, listed in attrs)
    When addMarker == False (patching), final size will be the longer of a, b
    """
    for idx, item in enumerate(b):
        try:
            attr = next((x for x in attrs if x in item), None)  # See if the item has any of the ID attributes
            match, matchIdx = next(((orgItm, idx) for idx, orgItm in enumerate(a) if attr in orgItm and orgItm[attr] == item[attr]), (None, None)) if attr else (None, None)
            if match and matchIdx != idx and addMarker: item[izipDestinationMatching] = izipDestinationMatching(attr, item[attr], matchIdx)
        except:
            match = None
        yield (match if match else a[idx] if len(a) > idx else None), item
    if not addMarker and len(a) > len(b):
        for item in a[len(b) - len(a):]:
            yield item, item


class DictHandle:
    """
        This is a utility class for operating on deep dictionaries
    """

    @staticmethod
    def find_path(data, target: str, mode) -> list:
        """Take a single path from the dictionary based on the target value"""
        path_iter = iter_node(data, [], target, mode)
        for path in path_iter:
            return path
        return []

    @staticmethod
    def find_all_path(data, target, mode) -> List[list]:
        """Take all path from the dictionary based on the target value"""
        path_iter = iter_node(data, [], target, mode)
        return list(path_iter)

    @staticmethod
    def find_by_path(data, path: list):
        """get value by path """

        def find_by_path(data, path):
            if not path:
                return data
            if isinstance(data, dict) and path[0] == "dict":
                return find_by_path(data, path[1:])
            if isinstance(data, dict) and path[0] in data:
                return find_by_path(data[path[0]], path[1:])
            if isinstance(data, list) and path[0] == 'list':
                result = find_by_path(random.choice(data), path[1:])
                if result:
                    return result
            return None

        return find_by_path(data, path)

    @staticmethod
    def dictdiff(a, b, searchAttrs=[], ignoreKeys=[]):
        """
        returns a dictionary which represents difference from a to b
        the return dict is as short as possible:
          equal items are removed
          added / changed items are listed
          removed items are listed with value=None
        Also processes list values where the resulting list size will match that of b.
        It can also search said list items (that are dicts) for identity values to detect changed positions.
          In case such identity value is found, it is kept so that it can be re-found during the merge phase
        @param a: original dict
        @param b: new dict
        @param searchAttrs: list of strings (keys to search for in sub-dicts)
        @param ignoreKeys: list of keys that should be ignored during dict comparison
        @return: dict / list / whatever input is
        """
        if not (isinstance(a, dict) and isinstance(b, dict)):
            if isinstance(a, list) and isinstance(b, list):
                return [DictHandle.dictdiff(v1, v2, searchAttrs, ignoreKeys) for v1, v2 in izip_destination(a, b, searchAttrs)]
            return b
        res = {}
        if izipDestinationMatching in b:
            keepKey = b[izipDestinationMatching].attr
            del b[izipDestinationMatching]
        else:
            keepKey = izipDestinationMatching
        for key in sorted(set(list(a.keys()) + list(b.keys()))):
            if key in ignoreKeys: continue
            v1 = a.get(key, None)
            v2 = b.get(key, None)
            if keepKey == key or v1 != v2: res[key] = DictHandle.dictdiff(v1, v2, searchAttrs, ignoreKeys)
        return res

    @staticmethod
    def dictmerge(a, b, searchAttrs=[], ignoreKeys=[]):
        """
        Returns a dictionary which merges differences recorded in b to base dictionary a
        Also processes list values where the resulting list size will match that of a
        It can also search said list items (that are dicts) for identity values to detect changed positions
        @param a: original dict
        @param b: diff dict to patch into a
        @param searchAttrs: list of strings (keys to search for in sub-dicts)
        @param ignoreKeys: list of keys that should be ignored during dict comparison
        @return: dict / list / whatever input is
        """
        if not (isinstance(a, dict) and isinstance(b, dict)):
            if isinstance(a, list) and isinstance(b, list):
                return [DictHandle.dictmerge(v1, v2, searchAttrs, ignoreKeys) for v1, v2 in
                        izip_destination(a, b, searchAttrs, False)]
            return b
        res = {}
        for key in sorted(set(list(a.keys()) + list(b.keys()))):
            v1 = a.get(key, None)
            if key in ignoreKeys:
                if v1 is not None: res[key] = v1
                continue
            v2 = b.get(key, None)
            # print "processing", key, v1, v2, key not in b, dictmerge(v1, v2)
            if v2 is not None:
                res[key] = DictHandle.dictmerge(v1, v2, searchAttrs, ignoreKeys)
            elif key not in b:
                res[key] = v1
        return res


def annotation_table_parse(annotation_table, api_path, api_method, field_name, location):
    data = DictHandle.find_by_path(annotation_table, [api_path, api_method])
    if data:
        for info in data:
            if info[field_name] == field_name and info[location] == location:
                return info['real_field_name']
    return None


def annotation_key_table_parse(annotation_key_table, api_path, api_method, field_name, location):
    data = DictHandle.find_by_path(annotation_key_table, [api_path, api_method])
    if data:
        for info in data:
            if info["field_name"] == field_name and info["location"] == location:
                return info['value']
    return None


def is_path_variable(_str):
    if not _str:
        return False
    if _str[0] == '{' and _str[-1] == '}' and len(_str)>2:
        return _str[1:-2]
    else:
        return False

def last_not_variable(_str: str):
    try:
        path = _str.split("/")
        for i in path[::-1]:
            if not is_path_variable(i) and i:
                return i
    except:
        return None


def random_dic(dicts):
    dict_key_ls = list(dicts.keys())
    random.shuffle(dict_key_ls)
    new_dic = {}
    for key in dict_key_ls:
        new_dic[key] = dicts.get(key)
    return new_dic
