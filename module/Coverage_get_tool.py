import requests
from bs4 import  BeautifulSoup

class GetCoverage:
    '''
    代码覆盖率测试工具 url = 'http://10.177.74.168:8000/'
    '''
    strhtml = None

    def getCoverages(self, url):
        try:
            strhtml = requests.get(url)
        except ConnectionError:
            return None
        soup = BeautifulSoup(strhtml.text, 'lxml')
        api_names = soup.select('#navgation > div > ul > li > a > label')
        api_coverages = soup.select('#navgation > div > ul > li > a > span')

        # print(api_names)
        # print(api_coverages)

        apis = []
        for name in api_names:
            name = str(name)
            list1 = name.split('>')
            list2 = list1[1].split('<')
            api_name = list2[0]
            # print(type(api_name))
            apis.append(api_name)

        coverages = []
        for cov in api_coverages:
            cov = str(cov)
            list1 = cov.split('>')
            list2 = list1[1].split('<')
            cover = list2[0]
            # print(type(cover))
            coverages.append(cover)

        '''
        dic存储{key：value}对应{api_name:api_coverage}  都是string类型
        '''
        dic_api_coverages = dict(zip(apis, coverages))
        return dic_api_coverages

    '''
    <label>执行总文件数：</label><span>277</span>
    <label>代码总行数：</label><span>185534</span>
    <label>可执行代码行数：</label><span>63104</span>
    <label>覆盖可执行代码行数：</label><span>13818</span>
    <label>可执行代码覆盖率：</label><span>21.9%</span>
    以字典存储
    前两项没啥用
    '''

    def getFile_total_num(self, url):
        try:
            strhtml = requests.get(url)
        except ConnectionError:
            return None
        soup = BeautifulSoup(strhtml.text, 'lxml')
        file_total_num = str(soup.select('body > div.sum > span:nth-child(2)')).split('>')[1].split('<')[0]
        return file_total_num

    def getCode_total_num(self, url):
        try:
            strhtml = requests.get(url)
        except ConnectionError:
            return None
        soup = BeautifulSoup(strhtml.text, 'lxml')
        code_total_num = str(soup.select('body > div.sum > span:nth-child(4)')).split('>')[1].split('<')[0]
        return code_total_num

    def getExecute_code_total_num(self, url):
        try:
            strhtml = requests.get(url)
        except ConnectionError:
            return None
        soup = BeautifulSoup(strhtml.text, 'lxml')
        execute_code_total_num = str(soup.select('body > div.sum > span:nth-child(6)')).split('>')[1].split('<')[0]
        return execute_code_total_num

    def getCoverage_executed_code_total_num(self, url):
        try:
            strhtml = requests.get(url)
        except ConnectionError:
            return None
        soup = BeautifulSoup(strhtml.text, 'lxml')
        coverage_executed_code_total_num = \
        str(soup.select('body > div.sum > span:nth-child(8)')).split('>')[1].split('<')[0]
        return coverage_executed_code_total_num

    def getCoverage_rate_executed_code(self, url):
        try:
            strhtml = requests.get(url)
        except ConnectionError:
            return None
        soup = BeautifulSoup(strhtml.text, 'lxml')
        try:
            coverage_rate_executed_code = \
                str(soup.select('body > div.sum > span:nth-child(10)')).split('>')[1].split('<')[0]
        except:
            coverage_rate_executed_code = '0.00%'

        return coverage_rate_executed_code

if __name__ == '__main__':
    get_coverage = GetCoverage()
    print(get_coverage.getCoverage_rate_executed_code('http://10.177.75.243:8000/'))
