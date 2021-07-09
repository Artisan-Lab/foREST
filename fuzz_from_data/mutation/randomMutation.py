import random

from mutation.mutation import Mutation


class RandomMutation(Mutation):
    """
    random
    """

    def __init__(self, data):
        self.data = data

    def result(self):
        """
        result implementation
        """
        print("random mutating...")

        return ''.join(i if random.randint(0, 1) else '\\' for i in self.data)
