"""
# nicht-up-to-date
App name: Zahlenratespiel

randomize(): bestimmt eine zahl zwischen 0 und 100
input(): fordert input an
compare(): vergleicht input mit randomize und führt win() oder loose() aus
win(): beglückwünscht den spieler und beendet das programm mit nächster eingabe
loose(): zeigt ein hinweis in der form 'input < x' bzw 'input > x' an








"""

import math as m
import random as rand
import typing


class Game(object):
    """Stellt das Zahlenratespiel an sich dar. Initialisiert die
    Dialog-sequenzen und die zu erratende Zahl. Letztere hat range(low, high).

    """

    # initialisiert für den Zahlenbereich 'zwischen 0 und 100'.
    def __init__(self,
                 state: object = None,
                 low: int = 1,
                 high: int = 99,
                 *args,
                 **kwargs):
        super().__init__()

        # Wird zum debuggen gebraucht.
        self.__state = state or rand.getstate()

        self.is_win = False

        # Übernimmt den Zahlenbereich range(low, high)
        self.low = low
        self.high = high

        self.number = self.get_number()
        self.is_gt_number = False

        # Initialisiert die Dialog-Generatoren.
        self.__dialog_start = ['Ich habe mir eine Zahl überlegt. Bin gespannt,'
                               ' wie schnell du sie erraten kannst.',
                               'Okay. ... Ach ja, du darfst natürlich wieder'
                               ' raten. Hätte ich beinahe vergessen.',
                               'Nene, dieses Mal ist meine Zahl'
                               ' um 7 größer. Ha!',
                               'Okay, Regeländerungen mag nicht jeder. '
                               'Kann ich verstehen. Back to the roots. Also?',
                               ]
        self.gen_start = self.__cycle_over(self.__dialog_start)

        self.__dialog_low = ['Knapp daneben. War etwas zuwenig.',
                             'Ich war so beschäftigt mit Pi. Deine Zahl war'
                             ' natürlich viel zu klein.',
                             'Pi ist wie ein rundes Gedicht. Einem wird '
                             'schwindelig bei den Kurven. ... Uhm, mehr!',
                             'Pi ist nicht so dein Ding? Ich habe da so ein'
                             ' Gefühl– dass deine Zahl zu klein ist.',
                             ]
        self.gen_low = self.__cycle_over(self.__dialog_low)

        self.__dialog_high = ['Knapp daneben. War etwas zuviel.',
                              'Ich war so beschäftigt mit Pi. Deine Zahl war'
                              ' natürlich viel zu groß.',
                              'Pi ist wie ein rundes Gedicht. Einem wird '
                              'schwindelig bei den Kurven. ... Uhm, weniger!',
                              'Pi ist nicht so dein Ding? Ich habe da so ein'
                              ' Gefühl– dass deine Zahl zu groß ist.',
                              ]
        self.gen_high = self.__cycle_over(self.__dialog_high)

        self.__dialog_end = ['Glückwunsch, du hast gewonnen!',
                             'Wow, nochmal gewonnen.',
                             'Ein schöner Tag, wenn man gewinnt, oder?',
                             'Respekt. Ich wäre nicht so schnell.',
                             ]
        self.gen_end = self.__cycle_over(self.__dialog_end)

        self.score_history: list[float] = []
        self.score_total: int = 0

        self.turn = 0

    def get_state(self):
        """Gibt den Status des Zufall-generators zurück.

        """
        return self.__state

    def get_number(self) -> int:
        """Verwendet im Kern den Mersenne Twister, um eine Zufallszahl mit
        ausgeglichener Distribution zu erzeugen.

        """
        return rand.randint(self.low, self.high)

    def get_next_dialog(self,
                        gen: typing.Generator,
                        is_skip=False,
                        skip_count=1) -> str:
        """Gibt abhängig vom Generator den nächsten Dialog-Entry aus. Kann
        ebenfalls Entries fallen lassen bzw. überspringen. Die Sprungweite ist
        standardmäßig auf 1, falls is_skip == True.

        """
        if is_skip:
            self.__skip_entry(gen, skip_count)
        return gen.__next__()

    def get_state(self) -> object:
        """Gibt den Status des verwendeten Zufall-generators wieder. Wird
        für gewöhnlich für Testcases verwendet.

        """
        return self.__state

    @staticmethod
    def __cycle_over(dialog: list[str]) -> typing.Generator[str, None, None]:
        """Gibt ein Generator-objekt zurück, welches endlos durch die
        gegebene Liste iteriert.

        """
        while True:
            for i in dialog:
                yield i

    @staticmethod
    def __skip_entry(gen: typing.Generator, count: int = 1):
        """Lässt entsprechend oft die Ergebnisse des Generators fallen. Default
        ist 1-mal.

        """
        for _ in range(count):
            gen.__next__()

    def get_dialog_text(self, val: int) -> str:
        """Verwendet einen integer-input, entscheidet über die Verhaltensweise,
        gibt einen entsprechenden Dialog-text zurück.

        Returns:
            Die Generatoren werden im Zuge alle bereits einen weiter geschaltet.

        """

        def set_action() -> None:
            """Entscheidet über die Verhaltensweise.

            """
            self.is_win = (val == self.number)
            self.is_gt_number = (val > self.number)

        self.turn += 1
        set_action()
        self.get_interim_result(val)
        if self.is_win:
            # um die Dialoglinien beizubehalten
            self.gen_start.__next__()
            self.gen_low.__next__()
            self.gen_high.__next__()

            self.score_total = self.evaluate_score()
            print(f'score_updated: {self.score_total}')

            return self.get_next_dialog(self.gen_end)
        elif self.is_gt_number:
            # um die Dialoglinien beizubehalten
            self.gen_start.__next__()
            self.gen_low.__next__()

            return self.get_next_dialog(self.gen_high)
        else:
            # um die Dialoglinien beizubehalten
            self.gen_start.__next__()
            self.gen_high.__next__()

            return self.get_next_dialog(self.gen_low)

    def get_accuracy(self, base: int, target: int, low: int, high: int) -> float:
        """Ermittelt die Abweichung des Targets von seiner Base, bezogen auf
        den Zahlenraum range(low, high). Die dargestellte Zahl gibt die
        Treffgenauigkeit in Prozent an.

        """
        # span ist die Größe des Zahlenraums.
        span = (high + 1) - low
        # difference ist der Unterschied von Base zu Target.
        difference = base - target

        # Entscheidet darüber, ob der Zahlenraum getroffen wurde.
        if base > high or base < low:
            percentile = 0.0
            # Penalty für extrem weit entfernte Zahlen.
            self.turn += 1
        else:
            percentile = (1 - (abs(difference) / span)) * 100.00
        return percentile

    def get_interim_result(self, val: int) -> float:
        """Ermittelt das Zwischenergebnis. Updated auch die score_history.

        """

        def add_to_score_history(num: float) -> None:
            """Updated die score_history.

            """
            self.score_history.append(round(num, 7))

        # Enthält die Treffgenauigkeit in Prozent (0.0 ~ 100.0).
        interim_result = self.get_accuracy(val, self.number, self.low,
                                           self.high)

        print(f'interim_res_in_history: {interim_result}')
        add_to_score_history(interim_result)

        return round(interim_result, 2)

    def evaluate_score(self) -> int:
        """Ermittelt das finale Ergebnis.

        """

        def get_weighted_avg_percentile() -> float:
            """Summiert und mittelt die bisherigen Teil-scores
            mit größerer Genauigkeit.

            """
            # BALANCE:
            # range(100.00 to avg 15.00 to 0.2)
            # first hit win, avg 5 hit with 75.00, 100 hits with 20.00

            total = m.fsum(self.score_history)

            res = total / (len(self.score_history) or 1)
            print(f'weighted_avg_perc: {res}')
            return res

        def get_weighted_sum_of_center_distances() -> float:
            """Verwendet eine Interpretation der Gaußschen Summenformel,
            um zur Summe aller möglichen Distanzen zu gelangen,
            die die ausgedachte Zufallszahl vom Zentrum zum Rand ihres
            Zahlenspektrums haben kann. Optimiert für große Zahlenspektren.

            """
            # BALANCE:
            # range(7.9 Mio to 62500 to avg 800 to 31)
            # span is 1-000-000, 1000, 100, 10

            # span ist die Größe des Zahlenraums.
            span = (self.high + 1) - self.low
            # center_point stellt die Mitte des Zahlenraums dar.
            center_point = span / 2

            # BALANCE:
            # range(500 Mrd to 2 Mio to avg 5000 to 50)
            # span is 1-000-000, 1000, 100, 10

            # Gaußsche SF.
            g_sum = center_point ** 2 * 2 + center_point

            # BALANCE:
            # range(63095.73 to 31.62 to 6.31 to 1.58)
            # span is 1-000-000, 1000, 100, 10

            length = len(str(span))
            span_to_self_length_relation = span ** ((length + 1) / 10)

            res = g_sum / span_to_self_length_relation

            print(f'weighted_center_dist_sum: {res}')
            return res

        def get_center_distance() -> float:
            """Zum Finden statistischer Ausreißer.

            """
            # BALANCE:
            # range(50.00 to 100.00)
            # edge_distance is center_point, low | high

            # Wählt die größte edge_distance in prozentualer Treffgenauigkeit.
            edge_distance_low = self.get_accuracy(self.number, self.low,
                                                  self.low, self.high)
            edge_distance_high = self.get_accuracy(self.number, self.high,
                                                   self.low, self.high)
            res = max(edge_distance_low, edge_distance_high)

            print(f'cur_center_dist: {res}')
            return res

        weighted_avg_percentile = get_weighted_avg_percentile()
        weighted_center_dist_sum = get_weighted_sum_of_center_distances()
        cur_center_dist = get_center_distance()
        PRIME = 47

        dividend = weighted_center_dist_sum * weighted_avg_percentile
        # Note: turn != len(score_history), wegen den hinzugefügten Penalties.
        divisor = (self.turn ** (100 / cur_center_dist)) * PRIME

        print(f'val1 / val2: {dividend}, {divisor}')
        score = dividend / divisor

        print(f'score: {score}')
        print(f'score_final: {int(score.__floor__())}')
        return int(score.__floor__())
