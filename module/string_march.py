


class StringMatch:

    @staticmethod
    def find_field_in_dic(dic, field_name, field_type):
        if isinstance(dic, dict):
            for key in dic:
                if key == field_name and type(dic[key].__name__) == field_type:
                    value = dic[key]
                    return value
                else:
                    value = StringMatch.find_field_in_dic(dic[key], field_name, field_type)
                    if value:
                        return value
        elif isinstance(dic, list):
            if (dic is not None) and (len(dic) > 0) and isinstance(dic[0], dict):
                for sub_dic in dic:
                    value = StringMatch.find_field_in_dic(sub_dic, field_name, field_type)
                    if value:
                        return value
        return None