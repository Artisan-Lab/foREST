from module.jsonhandle import JsonHandle


class Response:

    def __init__(self, request_message, response, api_info, success_pool, valid_pool):
        self.request_message = request_message
        if JsonHandle.json_judge(response):
            self.request_message = f'Received: \'HTTP/1.1 {response.status_code} response: {response.json()}\n\n\n'
        else:
            self.request_message = f'Received: \'HTTP/1.1 {response.status_code} response: {response}\n\n\n'
        self.response = response
        self.success_pool = success_pool
        self.valid_pool = valid_pool
        self.api_info = api_info

