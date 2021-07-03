from model.requestEntity import RequestEntity
from model.responseEntity import ResponseEntity


class MessageEntity:
    """
    desc a message
    """

    def __init__(self, req: RequestEntity, resp: ResponseEntity):
        self.requestEntity = req
        self.responseEntity = resp
