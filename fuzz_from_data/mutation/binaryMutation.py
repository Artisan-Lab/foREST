import os

from mutation.mutation import Mutation


class BinaryMutation(Mutation):
    """
    file or picture
    """

    def result(self):
        """
        result implementation
        """
        print("binary mutating...")
        with open('random.png', 'wb') as fout:
            fout.write(os.urandom(1024))
        return {'file': open('random.png', 'rb')}
