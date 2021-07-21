class make_url:

    # 组装url
    def make(self, url, p_location, p_name, value_fuzz, headers, data):
        flag = 0
        for i in range(len(p_location)):
            if p_location[i] == 0:
                url = url.replace('{' + p_name[i] + '}', str(value_fuzz[i]))
            elif p_location[i] == 1:
                # url追加?key1=value1&key2=value2到url后,即查询字符串
                if flag == 0:
                    flag = 1
                    url = url + "?" + str(p_name[i]) + "=" + str(value_fuzz[i])
                else:
                    url = url + "&" + str(p_name[i]) + "=" + str(value_fuzz[i])
            elif p_location[i] == 2:
                headers[str(p_name[i])] = value_fuzz[i]
            elif p_location[i] == 3:
                # 参数组成json字符串 ==> data
                if isinstance(data, dict):
                    data[str(p_name[i])] = value_fuzz[i]
                else:
                    if isinstance(value_fuzz[i], list) and value_fuzz[i]:
                        data.append(value_fuzz[i][0])
        headers['Content-Type'] = "application/json"
        return url, headers, data