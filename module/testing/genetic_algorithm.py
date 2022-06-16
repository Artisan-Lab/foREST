import random


class GeneticAlgorithm:

    def __init__(self, survival_points_list):
        self.survival_points_list_sum = 0
        self.survival_points_list = survival_points_list
        self.Roulette_Wheel_Selection_method()
        self.winner_sort_index = -1
        self.winner_index = 0
        self.winner_score = survival_points_list[0]

    def Roulette_Wheel_Selection_method(self):
        self.survival_points_list_sum = 0
        for i in self.survival_points_list:
            self.survival_points_list_sum += i
        random_number = random.uniform(0, self.survival_points_list_sum)
        current_sum = 0
        for i in range(len(self.survival_points_list)):
            current_sum += self.survival_points_list[i]
            if current_sum >= random_number:
                self.winner_index = i
                self.winner_score = self.survival_points_list[i]
                break

    def get_winner_index(self):
        self.Roulette_Wheel_Selection_method()
        return self.winner_index

    @property
    def get_survival_points_list(self):
        return self.survival_points_list

    def winner_success(self):
        self.winner_score = 10
        self.survival_points_list[self.winner_index] = self.winner_score
        self.Roulette_Wheel_Selection_method()

    def winner_failed(self):
        self.winner_score = self.survival_points_list[self.winner_index]
        self.winner_score -= pow(self.winner_score, 2)/20
        self.survival_points_list[self.winner_index] = self.winner_score
        self.Roulette_Wheel_Selection_method()




