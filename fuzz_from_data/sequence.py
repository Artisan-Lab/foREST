class Sequence:
    """
    a sequence number generator,
    and concurrency has not be considered
    """
    seq_num = 0

    @staticmethod
    def get_seq():
        """
        get seq number
        """
        Sequence.seq_num += 1
        return Sequence.seq_num
