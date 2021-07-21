import io
import json
import sys
import traceback

import requests as http_requests

from commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from model.requestEntity import RequestEntity
from myParser.myParserFactory import MyParserFactory
from commons.constants import *
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''


def main():
    """
    Execute R&R
    """
    log_parser = MyParserFactory.product_parser(LOG_PARSER_HW)
    log_parser.read_logs()
    requests = log_parser.parse()
    iteration_num = 1
    status_code_5xx_num = 0
    status_code_2xx_num = 0
    status_code_4xx_num = 0
    status_code_all = 0
    SUCCESS_num = 0
    FAILED_num = 0
    while True:
        try:
            print("execution phase start...")
            for i in range(len(requests)):
                try:
                    print(
                        f"executing {i + 1}/{len(requests)}/{iteration_num}, status_code_2xx_4xx_5xx_all {status_code_2xx_num}/{status_code_4xx_num}/{status_code_5xx_num}/{status_code_all}")
                    print(f'success_failed {SUCCESS_num}/{FAILED_num}')
                    request = requests[i]  # type: RequestEntity
                    if len(FUZZ_FROM_DATA_CONFIG.cookie) > 0:
                        print(f"using cookie {FUZZ_FROM_DATA_CONFIG.cookie}")
                        request.headers['Cookie'] = FUZZ_FROM_DATA_CONFIG.cookie
                    print(request)
                    request.headers.pop("x-forwarded-host", None)
                    request.headers.pop("host", None)
                    response = http_requests.request(method=request.method,
                                                     # url=FUZZ_FROM_DATA_CONFIG.base_url + request.url,
                                                     url=request.url,
                                                     data=str(request.body).encode(),
                                                     headers=request.headers)
                    print(response.text)
                    if 500 <= response.status_code <= 599:
                        status_code_5xx_num += 1
                        f = open("bugsLog/recording_and_replay_5xx.log", "a")
                        f.write(request.__str__())
                        f.close()
                        print("Server error,please check the log!")
                    elif 200 <= response.status_code <= 299:
                        status_code_2xx_num += 1
                        # parse response message
                        msg = json.loads(response.text)
                        if msg['status'] == 'FAILED':
                            FAILED_num += 1
                        if msg['status'] == 'SUCCESS':
                            SUCCESS_num += 1
                    elif 400 <= response.status_code <= 499:
                        status_code_4xx_num += 1
                    print('\n\n\n')

                except Exception as e:
                    print(traceback.format_exc())
                finally:
                    status_code_all += 1
            print("execution phase finished. next iteration start...")

        except Exception as e:
            print(traceback.format_exc())
            pass
        finally:
            iteration_num += 1


if __name__ == "__main__":
    main()
