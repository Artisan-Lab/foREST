from module.Coverage_get_tool import GetCoverage
import pymysql

'''
fuzz_monitor特点及功能：
    1.一个独立进程，且不会死掉，与fuzz测试本身无任何关系，仅用于代码覆盖率及测试用例选择
    2.监测并发线程测试过程中的代码覆盖率情况
'''
class Fuzz_monitor:
    '''
        监测并发线程测试过程中的代码覆盖率情况
        url：代码覆盖率测试工具地址  url = 'http://10.177.74.168:8000/'
        before_covrate：本次监测之前的代码覆盖率
        api_coverages：本次监测之前的所有api以及其对应的覆盖率 以字典形式存储
    '''
    def monitor(self,url):
        before_covrate = 0
        api_coverages = {}
        while True:
            if before_covrate == 0:
                covrate = GetCoverage.getCoverage_rate_executed_code(url)
                before_covrate = covrate
            else:
                covrate = GetCoverage.getCoverage_rate_executed_code(url)
                if covrate - before_covrate == 0:
                    pass
                else:
                    '''
                    说明覆盖率发生了变化，需要操作啦:
                        1.先得到现在所有api的coverage  以字典存储  {api_name:api_coverage}
                        2.查找导致覆盖率发生改变的api
                        3.更新之前的字典
                        4.得到该api的测试用例
                    '''
                    dic_api_coverages = GetCoverage.getCoverages(url)
                    apis = Fuzz_monitor.comparedic(api_coverages, dic_api_coverages)
                    api_coverages = dic_api_coverages
                    testcases = Fuzz_monitor.getTestCases(apis)
                    return testcases

    def comparedic(dic1, dic2):
        apis = []
        keys = dic2.keys()
        for key in keys:
            if dic1[key] != dic2[key]:
                apis.append(key)
        return apis

    def getTestCases(apis):
        ''' 打开数据库 '''
        conn = pymysql.connect(host='localhost', port=3306, database='restfulapitest',
                               user='root', passwd='123456', charset='utf8')
        cs1 = conn.cursor()
        cases = []
        for api_id in apis:
            case = cs1.execute('select body,url from restfulapitest where id = \'%s\'' % api_id)
            cases.append(case)
        return cases





