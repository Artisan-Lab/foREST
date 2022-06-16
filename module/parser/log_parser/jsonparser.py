from utils.jsonhandle import JsonHandle


def JsonParser(json_data):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    pass
                else:
                    JsonParser(value)
            elif isinstance(value, list):
                if len(value) == 0:
                    pass
                else:
                    for v in value:
                        JsonParser(v)
            elif isinstance(value, tuple):
                if len(value) == 0:
                    pass
                else:
                    for v in value:
                        JsonParser(v)
            elif isinstance(value, str):
                data = JsonHandle.is_json(value)
                if data:
                    JsonParser(data)
                    json_data[key] = data
    elif isinstance(json_data, list):
        if len(json_data) == 0:
            pass
        else:
            for v in json_data:
                JsonParser(v)
