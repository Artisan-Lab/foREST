from itertools import combinations

class Combination:
    def combine(temp_list, n):
        '''根据n获得列表中的所有可能组合（n个元素为一组）'''
        temp_list2 = []
        for c in combinations(temp_list, n):
            temp_list2.append(c)
        return temp_list2

    def get_combine(self, optional_list):
        end_list = []
        for i in range(len(optional_list)):
            end_list.extend(Combination.combine(optional_list, i))
        return (end_list)

