# from api import State, util
# from _paper_utils import run_experiment
# import random
# from . import load
# import progressbar
import sys
import os
# import pickle
import pickle5 as pickle
import pandas as pd

# print(bots_list)

def selectStrat(state, max_time, options):
    filename =  os.path.realpath('_paper_utils/copy_here_results_to_save_on_git/reps-' + str(options.repeats) + '_time-'+str(options.max_time)+'_players-'+options.players)
    bots_list, wins_list = pickle.loads(filename)

    col_list = ["rand_won", "bully_won", "rdeep_won", "ml_won"]
    df = pd.read_csv(filename, usecols=col_list)
    rand, bully, rdeep, ml = []
    res = None

    if max_time == 2:
        winner, points = state.winner()
        if winner == "rand":
            res = df["rand_won"].mean()
            rand[0] = res
        elif winner == "bully":
            res = df["bully_won"].mean()
            bully[0] = res
        elif winner == "rdeep":
            res = df["rdeep_won"].mean()
            rdeep[0] = res
        elif winner == "ml":
            res = df["ml_won"].mean()
            ml[0] = res
        return max(rand[0], bully[0], rdeep[0], ml[0])
    elif max_time == 5:
        if winner == "rand":
            res = df["rand_won"].mean()
            rand[0] = res
        elif winner == "bully":
            res = df["bully_won"].mean()
            bully[0] = res
        elif winner == "rdeep":
            res = df["rdeep_won"].mean()
            rdeep[0] = res
        elif winner == "ml":
            res = df["ml_won"].mean()
            ml[0] = res
        return max(rand[0], bully[0], rdeep[0], ml[0])
    elif max_time == 10:
        if winner == "rand":
            res = df["rand_won"].mean()
            rand[0] = res
        elif winner == "bully":
            res = df["bully_won"].mean()
            bully[0] = res
        elif winner == "rdeep":
            res = df["rdeep_won"].mean()
            rdeep[0] = res
        elif winner == "ml":
            res = df["ml_won"].mean()
            ml[0] = res
        return max(rand[0], bully[0], rdeep[0], ml[0])
    else:
        if max_time == 20:
            if winner == "rand":
            res = df["rand_won"].mean()
            rand[0] = res
        elif winner == "bully":
            res = df["bully_won"].mean()
            bully[0] = res
        elif winner == "rdeep":
            res = df["rdeep_won"].mean()
            rdeep[0] = res
        elif winner == "ml":
            res = df["ml_won"].mean()
            ml[0] = res
        return max(rand[0], bully[0], rdeep[0], ml[0])
