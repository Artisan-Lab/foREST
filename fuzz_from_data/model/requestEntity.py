class RequestEntity:
    """
    desc a request
    """

    def __init__(self, method, url, headers, body):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
    