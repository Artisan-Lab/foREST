from metamorphic.fuzz_and_judge import FuzzAndJudgeUnit
from metamorphic.metamorphic_compare import MetamorphicCompare


class FuzzMRParameter:

    fuzz_state = 1

    def __init__(self, parameter_field, base_url, source_response):
        self.parameter_field = parameter_field
        self.base_url = base_url
        self.source_response = source_response
        self.fuzz_unit = FuzzAndJudgeUnit(self.parameter_field, self.base_url)

    def get_sub_unit(self):
        for i in range(1, 11):
            self.fuzz_unit.exec()
            if self.fuzz_unit.responses_status == 0:
                self.fuzz_state = 0
                break
            compare_unit = MetamorphicCompare(self.source_response, self.fuzz_unit.request_response)
            compare_unit.subset_compare()
            if compare_unit.compare_result:
                break
            if not compare_unit.compare_result:
                print(self.fuzz_unit.new_url + '     Does not satisfy subset with source response')
                self.fuzz_state = 0
        return self.fuzz_unit

    def get_equivalence_unit(self):
        for i in range(1, 11):
            self.fuzz_unit.exec()
            if self.fuzz_unit.responses_status == 0:
                self.fuzz_state = 0
                break
            compare_unit = MetamorphicCompare(self.source_response, self.fuzz_unit.request_response)
            compare_unit.equivalence_compare()
            if compare_unit.compare_result:
                break
            if not compare_unit.compare_result and i == 10:
                print(self.fuzz_unit.new_url + '    Does not satisfy equivalence with source response')
                self.fuzz_state = 0
        return self.fuzz_unit

    def get_equality_unit(self):
        self.fuzz_unit.fuzz_default()
        if self.fuzz_unit.responses_status == 0:
            self.fuzz_state = 0
        else:
            compare_unit = MetamorphicCompare(self.source_response, self.fuzz_unit.request_response)
            compare_unit.equality_compare()
            if not compare_unit.compare_result:
                print(self.fuzz_unit.new_url + '   Does not satisfy equality with source response')
                self.fuzz_state = 0
        return self.fuzz_unit

    def get_disjoint_unit(self):
        fuzz_unit2 = FuzzAndJudgeUnit(self.parameter_field, self.base_url)
        for i in range(1,11):
            self.fuzz_unit.exec()
            fuzz_unit2.exec()
            if self.fuzz_unit.responses_status == 0 or fuzz_unit2.responses_status == 0:
                self.fuzz_state = 0
                break
            compare_unit = MetamorphicCompare(self.fuzz_unit.request_response, fuzz_unit2.request_response)
            compare_unit.disjoint_compare()
            if compare_unit.compare_result:
                break
            if not compare_unit.compare_result and i == 10:
                print('%s %s Does not satisfy disjoint' % (self.fuzz_unit.base_url, self.parameter_field.field_name))
                self.fuzz_state = 0
        return fuzz_unit2
