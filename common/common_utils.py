import json
class comutil:
    def has_intersec(list1,list2):
        for i in list1:
            if i in list2:
                return True
        return False

    def toJson(obj):
        # if type(obj) is list:
        #     tmp = []
        #     for i in obj:
        #         tmp.append(i.__dict__)
        #     return json.dumps(json.dumps(tmp))
        # else:
        #     return json.dumps(obj.__dict__)
        return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True,indent=4)

