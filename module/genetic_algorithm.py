import random


class GeneticAlgorithm:

    def __init__(self, survival_points_list):
        self.survival_points_list = survival_points_list
        self.survival_points_list_sum = 0
        self.winner_subscript = -1
        self.winner_score = -1

    def Roulette_Wheel_Selection_method(self):
        for i in self.survival_points_list:
            self.survival_points_list_sum += i
        random_number = random.uniform(0, self.survival_points_list_sum)
        current_sum = 0
        for i in range(len(self.survival_points_list)):
            current_sum += self.survival_points_list[i]
            if current_sum >= random_number:
                self.winner_subscript = i
                self.winner_score = self.survival_points_list[i]
                break

    def winner_success(self):
        self.winner_score += pow(10-self.winner_score, 2)/10
        self.survival_points_list[self.winner_subscript] = self.winner_score
        return self.survival_points_list

    def winner_failed(self):
        self.winner_score -= 0.5 + pow(5-self.winner_score, 2)/10
        self.survival_points_list[self.winner_subscript] = self.winner_score
        return self.survival_points_list

