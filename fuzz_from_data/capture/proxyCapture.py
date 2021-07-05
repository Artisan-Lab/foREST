import json
import os
import sys
import time

from mitmproxy import http

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from model.requestEntity import RequestEntity

captured_requests = []

log_json_file = f"{time.time()}-log.json"


class ProxyCapture:
    """
    use a proxy to capture http requests
    """

    def request(self, flow: http.HTTPFlow) -> None:
        request_headers = {}
        for k, v in flow.request.headers.items():
            request_headers[k] = v
        request_entity = RequestEntity(flow.request.method,
                                       flow.request.url,
                                       request_headers,
                                       flow.request.text)

        captured_requests.append(request_entity)

    def done(self):
        f = open(log_json_file, "a")
        f.write(json.dumps([ob.__dict__ for ob in captured_requests]))
        f.close()


addons = [ProxyCapture()]
