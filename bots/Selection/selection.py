from api import State, util
import random
from . import load

prev_results = getResults() # Results between which bots played, numeber of games, points of each bot, time segment, winner on avg

def selectStrat(prev_results, state):
    if prev_results.time() == 2:
        winner, points = state.winner()
        return winner
    else if prev_results.time() == 5:
        winner, points = state.winner()
        return winner
    else if prev_results.time() == 10:
        winner, points = state.winner()
        return winner
    else:
        if prev_results.time() == 20:
            winner, points = state.winner()
            return winner
