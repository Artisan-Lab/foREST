import json
from module.data_analysis.logpool import log_pool
from module.utils.jsonhandle import JsonHandle


def foREST_log_parser(path):
    f = open(path)
    line = True
    while line:
        line = f.readline()
        if 'Sending: ' in line:
            try:
                line_list = line.split()
                base_URL = line_list[6]
                path = line_list[5]
                time = line_list[0] + ' ' + line_list[1]
                http_method = line_list[4]
                line2 = f.readline()
                line2_list = line2.split('header:')
                header = line2_list[-1][:-1].replace('\'', '"')
                if header:
                    header = json.loads(header)
                    if 'Authorization' in header:
                        user_id = header['Authorization']
                    else:
                        user_id = None
                line3 = f.readline()
                data = line3[6:].replace("\n", "")
                if data and JsonHandle.is_json(data):
                    data = json.loads(data)
                line4 = f.readline()
                response_code = int(line4[20:23])
                response_data = line4[35:].replace('\'', '"')
                if JsonHandle.is_json(response_data):
                    response_data = json.loads(response_data)
                log_pool.save_foREST_log(http_method, base_URL, header, data, path, response_code, response_data, user_id)
            except:
                continue
    log_pool.user_classification()


