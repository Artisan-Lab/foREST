class ResponseEntity:
    """
    desc a request
    """

    def __init__(self, status_code, headers, content):
        self.status_code = status_code
        self.headers = headers
        self.content = content
