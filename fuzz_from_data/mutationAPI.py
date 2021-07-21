from difflib import SequenceMatcher
from fuzz_from_data.commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from fuzz_from_data.myParser.myParserFactory import MyParserFactory
from fuzz_from_data.model.requestEntity import RequestEntity
from fuzz_from_data import mutationTesting


def similar(a, b):
    """
    return the similarity of a & b
    """
    return SequenceMatcher(None, a, b).ratio()


def singleton(cls):
    """
    singleton implementation
    """
    _instance = {}

    def inner():
        """
        inner
        """
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class MutationAPI:
    """
    fuzzer can get some mutated log requests from the product log file
    """

    def __init__(self):
        log_parser = MyParserFactory.product_parser(FUZZ_FROM_DATA_CONFIG.log_parser_name)
        log_parser.read_logs()
        self.requests = log_parser.parse()
        self.cache = {}

    def get_matched_request(self, url) -> RequestEntity:
        """
        use a URL to match a log request
        """
        if url in self.cache:
            print(f'hitting the cache when matching url {url}')
            return self.cache[url]
        else:
            most_similar_request = None
            ratio = 0
            for item in self.requests:  # type:RequestEntity
                similarity = similar(url, item.url.split('?')[0] + "," + item.method)
                if similarity > ratio:
                    ratio = similarity
                    most_similar_request = item

            self.cache[url] = most_similar_request
            return mutationTesting.mutate_a_request(most_similar_request)

Mutation_API = MutationAPI()

if __name__ == "__main__":
    # api call demo
    mutationAPI = MutationAPI()
    print(mutationAPI.get_matched_request('/pipelineserv/api/v1/change,GET'))
    # when 2nd get,the cache will be hit
    print(mutationAPI.get_matched_request('/pipelineserv/api/v1/change,GET'))
