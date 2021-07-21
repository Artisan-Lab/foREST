import random
from urllib.parse import urlencode

from fuzz_from_data.commons import mutateConstants
from fuzz_from_data.commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from fuzz_from_data.commons.utils import Utils
from fuzz_from_data.mutation.mutation import Mutation


class QueryStringMutation(Mutation):
    """
    mutate query string e.g a=1&b=2
    """

    def __init__(self, query_string):
        self.queryString = query_string
        self.parsed_data = {x[0]: x[1] for x in [x.split("=") for x in query_string.split("&")]}

    def mutate_value(self):
        """
        random mutate value of a k-v
        """
        key = self.select_a_key_for_mutate()
        if key != '':
            if random.randint(0, 1) == 0:
                self.parsed_data[key] = random.choice(mutateConstants.INTEGERS_FOR_MUTATED)
            else:
                self.parsed_data[key] = random.choice(mutateConstants.STRINGS_FOR_MUTATED)

    def select_a_key_for_mutate(self):
        """
        select a k-v pair for mutation
        """
        dict_size = len(self.parsed_data)
        if dict_size <= 0:
            return ''
        else:
            random_index = random.randint(0, len(self.parsed_data) - 1)
            selected_key = ''
            for key, value in self.parsed_data.items():
                if random_index == 0:
                    print(f'{key}:{value} will be mutated!')
                    selected_key = key
                random_index -= 1
            return selected_key

    def drop(self):
        """
        random drop a k-v pair
        """
        need_dropped_key = self.select_a_key_for_mutate()
        if need_dropped_key != '':
            self.parsed_data.pop(need_dropped_key, None)

    def select(self):
        """
        only one k-v pair will be reserved
        """
        select_key = self.select_a_key_for_mutate()
        if select_key != '':
            for key in list(self.parsed_data.keys()):
                if key != select_key:
                    self.parsed_data.pop(key)

    def result(self):
        """
        convert python dict to querystring
        """
        return urlencode(self.parsed_data)

    def start(self):
        """
        start mutating
        """
        print("query string mutating...")
        if Utils.decision(FUZZ_FROM_DATA_CONFIG.query_string_drop_mutation_probability):
            self.drop()

        if Utils.decision(FUZZ_FROM_DATA_CONFIG.query_string_value_mutation_probability):
            self.mutate_value()

        if Utils.decision(FUZZ_FROM_DATA_CONFIG.query_string_selection_mutation_probability):
            self.select()
