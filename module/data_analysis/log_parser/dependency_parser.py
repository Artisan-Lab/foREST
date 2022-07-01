from entity.api_info import *
from module.parser.open_api_parse.api_parser import api_list_parser


class Sequence:

    def __init__(self):
        self.__api_sequence = []  # type: [APIInfo]
        self.__score = 0
        self.__parent_sequence = None
        self.__child_sequence = None
        self.__identifier_list = []

    def __getitem__(self, item):
        return self.__api_sequence[item]

    @property
    def identifier_list(self):
        return self.__identifier_list

    @identifier_list.setter
    def identifier_list(self, value):
        self.__identifier_list = value

    @property
    def parent_sequence(self):
        return self.__parent_sequence

    @parent_sequence.setter
    def parent_sequence(self, value):
        self.__parent_sequence = value

    @property
    def child_sequence(self):
        return self.__child_sequence

    @child_sequence.setter
    def child_sequence(self, value):
        self.__child_sequence = value

    @property
    def api_sequence(self):
        return self.__api_sequence

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value

    def append(self, api_info):
        self.__api_sequence.append(api_info)

    def add_score(self):
        self.__score += pow((1 - self.score), 2)

    def minus_score(self):
        self.__score -= pow(self.score, 2)


class LogDependencyParser:

    def __init__(self, api_dependency_info, parameter_dependency_info, api_list):
        self.__api_dependency_info = api_dependency_info
        self.__parameter_dependency_info = parameter_dependency_info
        self.__api_list = api_list  # type: [APIInfo]
        self.__sequence = {}
        self.api_dependency()
        self.parameter_dependency()

    def api_dependency(self):
        for sequence_len in self.__api_dependency_info:
            self.__sequence[sequence_len] = []
            for sequence in self.__api_dependency_info[sequence_len]:
                score = self.__api_dependency_info[sequence_len][sequence]
                api_info_sequence = Sequence()
                sequence_list = sequence.split(' --> ')
                for api_identifier in sequence_list:
                    api_info = api_list_parser().find_api_by_identifier(api_identifier)
                    if api_info:
                        api_info_sequence.append(api_info)
                    else:
                        break
                else:
                    if int(sequence_len) > 2:
                        for parent_sequence in self.__sequence[str(int(sequence_len)-1)]: # type: Sequence
                            if parent_sequence.identifier_list == sequence_list[:-1]:
                                parent_sequence.child_sequence = api_info_sequence
                                api_info_sequence.parent_sequence = parent_sequence
                    api_info_sequence.score = score
                    api_info_sequence.identifier_list = sequence_list
                    self.__sequence[sequence_len].append(api_info_sequence)
            self.__sequence[sequence_len].sort(key=lambda x: x.score, reverse=True)

    def parameter_dependency(self):
        for api_identifier in self.__parameter_dependency_info:
            api_info = api_list_parser().find_api_by_identifier(api_identifier)
            if api_info:
                pass
            else:
                continue
