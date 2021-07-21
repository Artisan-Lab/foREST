class RequestEntity:
    """
    desc a request
    """

    def __init__(self, method, url, headers, body):
        self.method = method
        self.url = url
        self.headers = headers # type:dict
        self.body = body # type:dict
        self.files = None

    def clone(self):
        """
        clone a new request entity
        """
        return RequestEntity(self.method, self.url, self.headers, self.body)

    def __str__(self) -> str:
        return f'{self.method} {self.url}\n{self.headers}\n{self.body}'
