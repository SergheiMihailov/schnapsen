#!usr/bin/env python
"""
A command line program for multiple games between several bots.

For all the options run
python play.py -h
"""

from argparse import ArgumentParser
from api import State, util, engine
import random, time

def run_tournament(options):

    botnames = options.players.split(",")

    bots = []
    for botname in botnames:
        bots.append(util.load_player(botname))

    n = len(bots)
    wins = [[0]*n for i in range(n)]
    avg_ms_move = [[0]*n for i in range(n)]
    times_late = [0]*n
    matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]
    totalgames = (n*n - n)/2 * options.repeats
    playedgames = 0

    for a, b in matches:
        for r in range(options.repeats):

            if random.choice([True, False]):
                p = [a, b]
            else:
                p = [b, a]

            # Generate a state with a random seed
            state = State.generate(phase=int(options.phase))

            winner, score, avg_ms_move_1, avg_ms_move_2, times_late_1, times_late_2 = engine.play(bots[p[0]], bots[p[1]], state, options.max_time, verbose=False, fast=options.fast)

            avg_ms_move[p[0]].append(avg_ms_move_1)
            avg_ms_move[p[1]].append(avg_ms_move_2)

            times_late[p[0]] += times_late_1
            times_late[p[1]] += times_late_2

            if winner is not None:
                loser = p[winner % 2]
                winner = p[winner - 1]
                wins[winner][loser] += score

            playedgames += 1

    return [str(bot).split('.')[1] for bot in bots], wins, map(lambda lst: sum(filter(lambda x: x > 0, lst))/len(lst), avg_ms_move), times_late

if __name__ == "__main__":

    ## Parse the command line options
    parser = ArgumentParser()

    parser.add_argument("-s", "--starting-phase",
                        dest="phase",
                        help="Which phase the game should start at.",
                        default=1)

    parser.add_argument("-p", "--players",
                        dest="players",
                        help="Comma-separated list of player names (enclose with quotes).",
                        default="rand,bully,rdeep")

    parser.add_argument("-r", "--repeats",
                        dest="repeats",
                        help="How many matches to play for each pair of bots",
                        type=int, default=10)

    parser.add_argument("-t", "--max-time",
                        dest="max_time",
                        help="maximum amount of time allowed per turn in milliseconds (default: 5000)",
                        type=int, default=5)

    parser.add_argument("-f", "--fast",
                        dest="fast",
                        action="store_true",
                        help="This option forgoes the engine's check of whether a bot is able to make a decision in the allotted time, so only use this option if you are sure that your bot is stable.")

    options = parser.parse_args()

    run_tournament(options)
