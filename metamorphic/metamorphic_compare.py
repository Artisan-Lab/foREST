class MetamorphicCompare():
    compare_result = None

    def __init__(self, response_1, response_2):
        self.response_1 = response_1
        self.response_2 = response_2

    def subset_compare(self):
        if (all([self.response_2[i] in self.response_1 for i in range(0, len(self.response_2))]) or
                all([self.response_1[i] in self.response_2 for i in range(0, len(self.response_1))])):
            self.compare_result = 1
        else:
            self.compare_result = 0

    def equality_compare(self):
        if self.response_1 == self.response_2:
            self.compare_result = 1
        else:
            self.compare_result = 0

    def equivalence_compare(self):
        if (all([self.response_1[i] in self.response_2 for i in range(0, len(self.response_1))]) and
            all([self.response_2[i] in self.response_1 for i in range(0, len(self.response_2))])) and \
                self.response_1 != self.response_2:
            self.compare_result = 1
        else:
            self.compare_result = 0

    def disjoint_compare(self):
        if (all([self.response_1[i] not in self.response_2 for i in range(0, len(self.response_1))]) and
                all([self.response_2[i] not in self.response_1 for i in range(0, len(self.response_2))])):
            self.compare_result = 1
        else:
            self.compare_result = 0

    def complete(self):
        if (all([self.response_1[i] in self.response_2 for i in range(0, len(self.response_1))]) and
            all([self.response_2[i] in self.response_1 for i in range(0, len(self.response_1))])) and \
                self.response_1 != self.response_2:
            self.compare_result = 1
        else:
            self.compare_result = 0