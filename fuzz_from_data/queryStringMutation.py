import random
import string
from urllib.parse import urlencode

import commons


class QueryStringMutation:
    """
    mutate query string e.g a=1&b=2
    """

    def __init__(self, query_string):
        self.queryString = query_string
        self.parsed_data = {x[0]: x[1] for x in [x.split("=") for x in query_string.split("&")]}

    def mutate_value(self):
        """
        random drop a k-v pair
        """

        random_index = random.randint(0, len(self.parsed_data) - 1)
        need_mutate_key = ''
        for key, value in self.parsed_data.items():
            if random_index == 0:
                print(f'{key}:{value} will be mutate_value!')
                if random.randint(0, 1) == 0:
                    self.parsed_data[key] = random.choice(commons.mutateConstants.INTEGERS_FOR_MUTATED)
                else:
                    self.parsed_data[key] = ''.join(
                        [random.choice(string.ascii_letters + string.digits) for n in range(32)])
            random_index -= 1

    def drop(self):
        """
        random drop a k-v pair
        """

        random_index = random.randint(0, len(self.parsed_data) - 1)
        need_dropped_key = ''
        for key, value in self.parsed_data.items():
            if random_index == 0:
                print(f'{key}:{value} will be dropped!')
                need_dropped_key = key
            random_index -= 1
        if need_dropped_key != '':
            self.parsed_data.pop(need_dropped_key, None)

    def select(self):
        """
        only one k-v pair will be reserved
        """
        random_index = random.randint(0, len(self.parsed_data) - 1)
        select_key = ''
        for key, value in self.parsed_data.items():
            if random_index == 0:
                print(f'{key}:{value} will be selected!')
                select_key = key
            random_index -= 1
        if select_key != '':
            for key in list(self.parsed_data.keys()):
                if key != select_key:
                    self.parsed_data.pop(key)

    def dump(self):
        return urlencode(self.parsed_data)
