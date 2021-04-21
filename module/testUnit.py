import requests
import random


def random_date(start, end):
    # 随机生成start与end之间的日期 format：ISO 8601
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def random_str(slen=10):
    # 随机生成字符串，默认长度为10
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(slen):
        sa.append(random.choice(seed))
    return ''.join(sa)


class FuzzAndJudgeUnit:

    def __init__(self, field_info, base_url, req_field_names):
        self.field_info = field_info
        self.base_url = base_url
        self.req_field_names = req_field_names
        self.parameter = None
        self.responses_status = None

    def fuzz_parameter(self):
        if self.field_info.enum:
            self.parameter = self.field_info.field_name + '=' + str(random.choice(self.field_info.enum))
        elif self.field_info.format:
            if field_info.format == 'ISO 8601 YYYY-MM-DDTHH:MM:SSZ':
                self.parameter = self.field_info.field_name + '=' + \
                       str(random_date(
                           datetime(2021, 12, 31, 23, 59, 59).astimezone().replace(microsecond=0)).isoformat())
        else:
            if self.field_info.field_type == 'boolean':
                self.parameter = self.field_info.field_name + '=' + random.choice(['true', 'false'])
            elif self.field_info.field_type == 'string':
                self.parameter = self.field_info.field_name + '=' + random_str()
            elif self.field_info.field_type == 'integer':
                self.parameter = self.field_info.field_name + '=' + str(random.randint(0, 50))
        pass

    def add_parameter(self):
        if self.field_info.location == 0:
            self.base_url = self.base_url.replace('{' + self.field_info.field_name + '}', self.parameter)
        else:
            self.base_url = self.base_url + '&' + self.parameter

    def judge_effective(self):
        request_response = requests.get(self.base_url)
        response_status = request_response.status_code
        if 300 > response_status >= 200:
            if not json.loads(request_response.text):
                self.responses_status = 0
            else:
                self.responses_status = 1
                return request_response
        elif 500 > response_status >= 300:
            self.responses_status = 0
        elif 500 == response_status:
            print('find bug in %s' % url1)

    def add_token(self):
        # 加上token 因为暂时不考虑token的问题 所以在第一步就加上token
        # if '?' in url:
        #     url = url + '&private_token=n19y6WJgSgjyDuFSHMx9'
        #     # ehWyDYxYMRcFLKCRryeK root token
        # else:
        self.base_url = self.base_url + '?private_token=n19y6WJgSgjyDuFSHMx9'

    def exec_test(self):
        FuzzAndJudge.fuzz_parameter()
        FuzzAndJudge.add_parameter()
        FuzzAndJudge.judge_effective()


def MR_texting(response_text, response_text1, response_text2, MR_matric):
    # MR_matric 的 含义分别为 subset  equality equivalence disjoint complete diffirence
    response_text3 = response_text1 + response_text2
    if (all([response_text[i] in response_text1 for i in range(0,len(response_text))]) or \
            all([response_text1[i] in response_text for i in range(0, len(response_text1))])):
        # judge subset
        MR_matric[0] = MR_matric[0] + 1
    if response_text == response_text1:
        MR_matric[1] = MR_matric[1] + 1
    if (all([response_text[i] in response_text1 for i in range(0,len(response_text))]) and
            all([response_text1[i] in response_text for i in range(0,len(response_text1))])) and \
            response_text1 != response_text:
        MR_matric[2] = MR_matric[2] + 1
    if (all([response_text2[i] not in response_text1 for i in range(0,len(response_text2))]) and
            all([response_text1[i] not in response_text2 for i in range(0,len(response_text1))])):
        MR_matric[3] = MR_matric[3] + 1
    if (all([response_text[i] in response_text3 for i in range(0,len(response_text))]) and
            all([response_text3[i] in response_text for i in range(0,len(response_text3))])) and \
            response_text1 != response_text2:
        MR_matric[4] = MR_matric[4] + 1
    return MR_matric


def metamorphic(api_info,parameter_list):
    if api_info.http_method == 'get':
        MR_dic = {}
        url = add_token(api_info.path)
        if api_info.req_field_names:
            for req_paramerter in api_info.req_param:
                if req_paramerter.field_name in api_info.req_field_names:
                    parameter = str(parameter_list[req_paramerter.field_name])
                    if req_paramerter.location == 0:
                        url = url.replace('{'+req_paramerter.field_name+'}',parameter)
                    else:
                        url = url + '&' + parameter
        source_response = requests.get(url)
        if source_response.status_code > 300:
            print(url + 'dependency default')
            return
        for req_paramerter in api_info.req_param:
            # 测API的每个参数
            MR_matric_count = [0, 0, 0, 0, 0, 0]
            # 前三个为源输出与加参数输出之间的关系 subset equality equivalence
            # 不同参数输出之间的关系 disjoint
            # 不同参数输出与源输出之间的关系 complete
            # 多次相同请求之间的关系difference
            MR_matric = [0, 0, 0, 0, 0, 0]
            # 记录测得的MR
            if req_paramerter.field_name in api_info.req_field_names:
                continue
            responses = [json.loads(requests.get(url).text)]
            for i in range(1,11):
                a = FuzzAndJudgeUnit(api_info.req_parameter)
                responses = get_responses(url, req_paramerter, responses, 0)
            if len(responses) < 10:
                print('lack %s' % req_paramerter.field_name)
                continue
            for i in range(1, 11):
                response_text = responses[0]
                response_text1 = random.choice(responses[1:11])
                response_text2 = random.choice(responses[1:11])
                for i in range(10):
                    if response_text1 == response_text2:
                        response_text2 = random.choice(responses[1:11])
                MR_matric_count = MR_texting(response_text, response_text1, response_text2, MR_matric_count)
            if MR_matric_count[0] == max(MR_matric_count): #and MR_matric_count[1] + MR_matric_count[2] <MR_matric_count[0]:
                MR_matric[0] = 1
            if MR_matric_count[1] == max(MR_matric_count):
                MR_matric[1] = 1
            if MR_matric_count[1] + MR_matric_count[2] == MR_matric_count[0] and MR_matric_count[1] != 0 and MR_matric_count[2] !=0:
                MR_matric[2] = 1
            if MR_matric_count[3] == max(MR_matric_count):
                MR_matric[3] = 1
            if MR_matric_count[4] == 10 and MR_matric_count[2] != 1:
                MR_matric[4] = 1
            MR_dic[str(req_paramerter.field_name)] = MR_matric
        print(str(MR_dic))



path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/projects-api.yaml")
api_list = parse.get_api_info(1, path)
for api_info in api_list:
    metamorphic(api_info, {'user_id': 34})




