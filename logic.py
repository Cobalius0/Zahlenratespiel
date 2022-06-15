"""
App name: Zahlenratespiel

randomize(): bestimmt eine zahl zwischen 0 und 100
input(): fordert input an
compare(): vergleicht input mit randomize und führt win() oder loose() aus
win(): beglückwünscht den spieler und beendet das programm mit nächster eingabe
loose(): zeigt ein hinweis in der form 'input < x' bzw 'input > x' an








"""

import tkinter as tk
import secrets as sec
import math as m

SCORE_WEIGHT_MULTI = 724978214
SCORE_WEIGHT_ADDI = 580  # Note: Muss größer 0 sein.


class Opponent(object):
    def __init__(self, min_num=1, max_num=109):
        def get_idea() -> int:
            return sec.randbelow(max_num + 1) + min_num

        self.on_mind = 1 # get_idea()
        print('idea: ', self.on_mind)
        self.min_num = min_num
        self.max_num = max_num
        self.pool_size = max_num - min_num + 1
        self.turn = 0
        self.score_history = []
        self.score_total = 0

    # def take_turn(self, user_input):
    #     if self.react(user_input):
    #         self.turn += 1
    #         self.take_turn(user_input)
    #     print(f'Du brauchtest {self.turn} Versuche. ')

    # lässt nur positive integerwerte durch.
    @staticmethod
    def get_valid_input() -> int:
        res: str
        while True:
            res = input()
            if res.startswith('-') or not res.isdecimal():
                print(f'Bitte gebe eine positive, ganze Zahl ein. ')
                continue
            else:
                break
        return int(res)

    def run(self) -> int:
        print(f'Ich habe mir eine Zahl überlegt. Bin gespannt, wie schnell du sie erraten kannst. ')
        while True:
            self.turn += 1
            info = self.get_valid_input()
            print('input: ', info)
            reaction = self.react_to(info)
            print('reaction: ', reaction)
            interim_result = self.get_interim_result(info)
            print('inter_res: ', interim_result)
            if reaction is False:
                break
        res = self.evaluate_score()
        print('final_score: ', res)
        return res

    def react_to(self, info) -> bool:
        def choose_option(option) -> bool:
            match option:
                case None:
                    print(f'Glückwunsch, gewonnen. ')
                    return False
                case True:
                    print(f'Etwas zuviel. ')
                    return True
                case False:
                    print(f'Etwas zuwenig. ')
                    return True

        if info == self.on_mind:
            return choose_option(None)
        elif info > self.on_mind:
            return choose_option(True)
        else:
            return choose_option(False)

    def get_interim_result(self, info) -> float:
        def get_accuracy(base, target, high, low, span) -> float:
            difference: int = base - target
            if base > high or base < low:
                percentile = 0.0
            else:
                percentile = (1 - (difference.__abs__() / span)) * 100.00
            return percentile

        interim_result = get_accuracy(info,
                                      self.on_mind,
                                      self.max_num,
                                      self.min_num,
                                      self.pool_size)
        self.score_history += [interim_result.__round__(7)]
        print('score_his_up: ', self.score_history)
        print('len_his: ', len(self.score_history))
        return interim_result.__round__(2)

    # Ermittelt den finalen score.
    def evaluate_score(self) -> int:

        # Summiert und mittelt die bisherigen Teil-scores mit größerer Genauigkeit.
        def get_avg_percentile() -> float:
            total = m.fsum(self.score_history)
            res = total / len(self.score_history)
            print('avg_perc: ', res)
            return res

        # Verwendet eine Interpretation der Gaußschen Summenformel,
        # um zur Summe aller möglichen Distanzen zu gelangen, die die ausgedachte
        # Zahl (on_mind) vom Zentrum zum Rand ihres Zahlenspektrums haben kann.
        # Optimiert für große Zahlenspektren.
        def get_sum_of_center_distances() -> float:
            center_point = self.pool_size / 2
            res = center_point ** 2 * 2 + center_point  # Gaußsche SF.
            print('sum_cen_dis: ', res)
            return res

        # Verwendet eine Projektion von [0, inf) auf [0, 1],
        # um das Finden möglicher statistischer Ausreißer zu belohnen.
        def get_weighted_center_distance_reward() -> float:
            cur_edge_distance = self.pool_size - self.on_mind
            try:
                infinity_to_zero = (self.pool_size / cur_edge_distance) - 1
            except ZeroDivisionError:
                infinity_to_zero = m.inf
            one_to_zero = m.atan(infinity_to_zero) / (m.pi / 2)

            print(one_to_zero)

            # Note: Game Balance.
            spectrum_size_relation_to_length = (self.pool_size ** (1 + (len(str(self.pool_size))) / 10))
            print('BALANCE: ', spectrum_size_relation_to_length)
            res = one_to_zero * (SCORE_WEIGHT_MULTI / (spectrum_size_relation_to_length * 100)) + SCORE_WEIGHT_ADDI

            print('weighted_rev: ', res)
            return res

        avg_percentile = get_avg_percentile()
        sum_of_center_distances = get_sum_of_center_distances()
        weighted_center_distance_reward = get_weighted_center_distance_reward()

        score = (sum_of_center_distances * avg_percentile) / (self.turn * weighted_center_distance_reward)
        print('turn: ', self.turn)
        print('score_precise: ', score)
        return int(score.__floor__())


def new_game():
    op = Opponent()
    res = op.run()
    print('op_res: ', res)
