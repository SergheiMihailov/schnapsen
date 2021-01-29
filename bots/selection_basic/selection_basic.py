"""
Selection Basic Bot
"""

# Import the API objects

from api import util

from bots import *

# explicit model to make loading faster
SELECTION_MODEL = {1: {'times_late': [720, 744, 782, 754], 'scores': [2340, 2268, 2154, 2238], 'ms_per_move': [0.005547389863653386, 0.005707902477142659, 0.006029692894600807, 0.005780658823378543], 'bot_names': ['rand', 'bully', 'rdeep', 'ml']}, 2: {'times_late': [739, 767, 781, 713], 'scores': [2283, 2199, 2157, 2361], 'ms_per_move': [0.006268510951640758, 0.006758061970802064, 0.0066297858002338, 0.006056029428827002], 'bot_names': ['rand', 'bully', 'rdeep', 'ml']}, 100: {'times_late': [0, 0, 0, 2], 'scores': [574, 942, 1889, 1685], 'ms_per_move': [0.018881095502565514, 0.01837085895592579, 0.030999596224995592, 0.045223730429995536], 'bot_names': ['rand', 'bully', 'rdeep', 'ml']}, 5: {'times_late': [373, 427, 1112, 1024], 'scores': [3210, 3157, 1164, 1428], 'ms_per_move': [0.00962074308881674, 0.009897317321972944, 0.012095519361343789, 0.011462855687800875], 'bot_names': ['rand', 'bully', 'rdeep', 'ml']}, 200: {'times_late': [0, 0, 0, 4], 'scores': [605, 1003, 1918, 1666], 'ms_per_move': [0.019858061502527283, 0.02060038155238545, 0.03306443877442123, 0.05481818619426867], 'bot_names': ['rand', 'bully', 'rdeep', 'ml']}, 10: {'times_late': [10, 8, 1242, 1246], 'scores': [3248, 3646, 774, 762], 'ms_per_move': [0.013028636000385271, 0.013158912042628285, 0.017962453213143856, 0.01989038927969358], 'bot_names': ['rand', 'bully', 'rdeep', 'ml']}, 50: {'times_late': [0, 0, 4, 227], 'scores': [1013, 1062, 2059, 1333], 'ms_per_move': [0.01945485736865252, 0.019844273161816146, 0.03362794203725998, 0.047255297881873916], 'bot_names': ['rand', 'bully', 'rdeep', 'ml']}, 20: {'times_late': [1, 0, 518, 1427], 'scores': [2348, 3067, 2179, 219], 'ms_per_move': [0.017320900186154026, 0.017252645203110855, 0.027818278606453438, 0.03217961880649235], 'bot_names': ['rand', 'bully', 'rdeep', 'ml']}}

class Bot:

    __model = None

    def __init__(self):
        # Load the model
        self.__model = SELECTION_MODEL

    def get_move(self, state):

        max_times_in_model = sorted(self.__model.keys())

        bot_to_use_name = 'rand'

        for i in range(len(max_times_in_model) - 1):
            if max_times_in_model[i + 1] > state.get_max_time() or i + 2 == len(max_times_in_model):
                matching_model_time = max_times_in_model[i]
                matching_bot_scores = self.__model[matching_model_time]['scores']
                # print(matching_bot_scores)
                bot_to_use_name = self.__model[matching_model_time]['bot_names'][
                    matching_bot_scores.index(max(matching_bot_scores))]
                break
        # print(state.get_max_time())
        # print(bot_to_use_name)
        bot_to_use = util.load_player(bot_to_use_name)

        return bot_to_use.get_move(state)