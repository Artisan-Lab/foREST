from itertools import combinations

'''
组合所有optional参数
为防止组合爆炸，可设定优先级，并采用BFS等方式选取组合
'''
class Combination:
    def combine(self, temp_list, n):
        '''根据n获得列表中的所有可能组合（n个元素为一组）'''
        temp_list2 = []
        for c in combinations(temp_list, n):
            temp_list2.append(c)
        return temp_list2

    def get_combine(self, optional_list, times):
        end_list = []
        for i in range(times):
            end_list.extend(Combination.combine(optional_list, i))
        return end_list

