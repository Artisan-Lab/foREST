import requests as http_requests

from commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from model.requestEntity import RequestEntity
from parser.apacheLogParser import ApacheLogParser


def get_requests_from_apache_log(log_src):
    """
    requests parsed from apache error.log
    """
    log_parser = ApacheLogParser(log_src)
    log_parser.read_logs()
    return log_parser.parse()


def main():
    requests = get_requests_from_apache_log(FUZZ_FROM_DATA_CONFIG.log_path)
    iteration_num = 1
    while True:
        try:
            print("execution phrase start...")
            total_requests = requests
            for i in range(len(total_requests)):
                try:
                    print(f"executing {i + 1}/{len(total_requests)}/{iteration_num}")
                    request = total_requests[i]  # type: RequestEntity
                    if len(FUZZ_FROM_DATA_CONFIG.cookie) > 0:
                        print(f"using cookie {FUZZ_FROM_DATA_CONFIG.cookie}")
                        request.headers['Cookie'] = FUZZ_FROM_DATA_CONFIG.cookie
                    print(request)
                    response = http_requests.request(method=request.method,
                                                     url=FUZZ_FROM_DATA_CONFIG.base_url + request.url,
                                                     data=request.body,
                                                     headers=request.headers)
                    print(response)
                    if response.status_code == 503:
                        print("Server error,please check the log!")
                    print('\n\n\n')
                except Exception as e:
                    print(e)
                    pass
            print("execution phrase finished. next iteration start...")
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    main()
