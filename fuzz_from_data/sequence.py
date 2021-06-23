"""
a sequence number generator,
and concurrency has not be considered
"""


class Sequence:
    seq_num = 0

    @staticmethod
    def get_seq():
        Sequence.seq_num = Sequence.seq_num + 1
        return Sequence.seq_num
