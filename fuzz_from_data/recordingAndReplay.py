import requests as http_requests

from commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from model.requestEntity import RequestEntity
from parser.apacheLogParser import ApacheLogParser
from parser.proxyLogParser import ProxyLogParser


def get_requests_from_apache_log(log_src):
    """
    requests parsed from apache error.log
    """
    log_parser = ApacheLogParser(log_src)
    log_parser.read_logs()
    return log_parser.parse()


def get_requests_from_proxy_log(log_src):
    """
        requests parsed from proxy.log
        """
    log_parser = ProxyLogParser(log_src)
    log_parser.read_logs()
    return log_parser.parse()


def main():
    """
    main()
    """
    # requests = get_requests_from_apache_log(FUZZ_FROM_DATA_CONFIG.log_path)
    # requests = get_requests_from_proxy_log(FUZZ_FROM_DATA_CONFIG.log_path)
    # TODO: flexible configuration for string & list
    requests = get_requests_from_proxy_log(
        ['/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625407119.9178529-log.json',
         '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625407979.8544893-log.json',
         '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625408541.4782267-log.json',
         '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625409134.9770634-log.json',
         '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625409454.4674275-log.json',
         '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625409738.8814836-log.json',
         '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625410012.0339994-log.json',
         '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625410369.94529-log.json'])
    iteration_num = 1
    status_code_5xx_num = 0
    status_code_2xx_num = 0
    status_code_all = 0
    while True:
        try:
            print("execution phrase start...")
            total_requests = requests
            for i in range(len(total_requests)):
                try:
                    print(
                        f"executing {i + 1}/{len(total_requests)}/{iteration_num}, status_code_2xx_5xx_all {status_code_2xx_num}/{status_code_5xx_num}/{status_code_all}")
                    request = total_requests[i]  # type: RequestEntity
                    if len(FUZZ_FROM_DATA_CONFIG.cookie) > 0:
                        print(f"using cookie {FUZZ_FROM_DATA_CONFIG.cookie}")
                        request.headers['Cookie'] = FUZZ_FROM_DATA_CONFIG.cookie
                    print(request)
                    response = http_requests.request(method=request.method,
                                                     # url=FUZZ_FROM_DATA_CONFIG.base_url + request.url,
                                                     url=request.url,
                                                     data=request.body,
                                                     headers=request.headers)
                    print(response)
                    if 500 <= response.status_code <= 599:
                        status_code_5xx_num += 1
                        f = open("bugsLog/recording_and_replay_5xx.log", "a")
                        f.write(request.__str__())
                        f.close()
                        print("Server error,please check the log!")
                    elif 200 <= response.status_code <= 299:
                        status_code_2xx_num += 1
                    print('\n\n\n')

                except Exception as e:
                    print(e)
                    pass
                finally:
                    status_code_all += 1
            print("execution phrase finished. next iteration start...")

        except Exception as e:
            print(e)
            pass
        finally:
            iteration_num += 1


if __name__ == "__main__":
    main()
