from typing import List


class APIDependency:

    def __init__(self, api_identifier):
        self.api_identifier = api_identifier
        self.depend_list = {}

    def __eq__(self, other):
        return self.depend_list == other.depend_list

    def append(self, param_identifier, target_identifier):
        if param_identifier not in self.depend_list:
            self.depend_list[param_identifier] = target_identifier


class Sequence:

    def __init__(self):
        self.__id = -1
        self.__api_list = []
        self.__testing_time = 0
        self.__success_time = 0
        self.__success_rate = 0
        self.count = 1
    
    def __eq__(self, other):
        return self.__api_list == other.__api_list

    def __len__(self):
        return len(self.__api_list)

    def append(self, api: APIDependency):
        self.__api_list.append(api)

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value
    
    @property
    def api_list(self):
        return self.__api_list

    @property
    def testing_time(self):
        return self.__testing_time

    @testing_time.setter
    def testing_time(self, value):
        self.__testing_time = value

    @property
    def success_time(self):
        return self.__success_time

    @success_time.setter
    def success_time(self, value):
        self.__success_time = value

    @property
    def success_rate(self):
        self.__success_rate = self.__success_time / self.testing_time
        return self.__success_rate


class SequenceMonitor:
    __instance = None
    """
        testing sequence class
        Used to control testing sequence
    """

    @staticmethod
    def Instance():
        """ Singleton's instance accessor

        @return Sequence Monitor instance
        @rtype  Sequence Monitor

        """
        if SequenceMonitor.__instance is None:
            raise Exception("sequence Monitor not yet initialized.")
        return SequenceMonitor.__instance

    def __init__(self):
        if self.__instance:
            raise Exception("Attempting to create a new singleton instance.")
        self.__sequence_list = []  # type: List[Sequence]
        self.__sequence_len_dict = {}
        self.__new_sequence_id = 0
        SequenceMonitor.__instance = self

    def append_sequence(self, sequence: Sequence):
        for exist_sequence in self.__sequence_list:
            if sequence == exist_sequence:
                exist_sequence.count += 1
                return
        sequence.id = self.__new_sequence_id
        self.__new_sequence_id += 1
        self.__sequence_list.append(sequence)
        if len(sequence) not in self.__sequence_len_dict:
            self.__sequence_len_dict[len(sequence)] = []
        self.__sequence_len_dict[len(sequence)].append(sequence)

    def append_sequences(self, sequence_list: List[Sequence]):
        for sequence in sequence_list:
            self.append_sequence(sequence)


def Sequence_Monitor() -> SequenceMonitor:
    """ Accessor for the Sequence monitor singleton """
    return SequenceMonitor.Instance()


    
    
        





