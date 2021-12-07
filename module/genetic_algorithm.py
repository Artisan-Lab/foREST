import random


class GeneticAlgorithm:

    def __init__(self, survival_points_list):
        self.survival_points_list = survival_points_list
        self.depend_sort = [i for i in range(len(survival_points_list))]
        self.Roulette_Wheel_Selection_method()
        self.depend_sort.reverse()
        self.winner_sort_index = -1
        self.winner_index = self.depend_sort[self.winner_sort_index]
        self.winner_score = self.survival_points_list[self.winner_index]

    def Roulette_Wheel_Selection_method(self):
        self.depend_sort = sorted(range(len(self.survival_points_list)), key=lambda k: self.survival_points_list[k])

    def get_next_winner_index(self):
        self.winner_sort_index += 1
        self.winner_index = self.depend_sort[self.winner_sort_index]
        self.winner_score = self.survival_points_list[self.winner_index]
        return self.winner_index

    @property
    def get_survival_points_list(self):
        return self.survival_points_list

    def winner_success(self):
        self.winner_score = self.survival_points_list[self.winner_index]
        self.winner_score += pow(10-self.winner_score, 2)/10
        self.survival_points_list[self.winner_index] = self.winner_score

    def winner_failed(self):
        self.winner_score = self.survival_points_list[self.winner_index]
        self.winner_score -= pow(self.winner_score, 2)/20
        self.survival_points_list[self.winner_index] = self.winner_score




