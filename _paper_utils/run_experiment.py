#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import progressbar
import pickle

sys.path.append(os.path.realpath('.'))

from tournament import run_tournament
from argparse import ArgumentParser
from output_formatters import wins_to_csv

def run_experiment(options, is_batch = False):
    options.phase = 1
    options.fast = False

    filename =  os.path.realpath('_paper_utils/results/reps-' + str(options.repeats) + '_time-'+str(options.max_time)+'_players-'+options.players)
    filename_pkl = filename+'.pkl'
    if (not is_batch):
        if os.path.exists(filename_pkl):
            print('♻️\tExperiment file already exists: \n\t'+filename_pkl)

            try:
                input = raw_input
                if (input('\n\tRewrite? (y/N) ') != 'y'): 
                    return 
            except NameError:
                pass

        print('🧪\tRunning experiment...')

    result = run_tournament(options)

    open(filename_pkl, 'w').write(pickle.dumps(result))
    
    wins_to_csv(filename, result)

    if not is_batch: print('✨\tExperiment finished!  \n\tData saved in '+filename)

REPEATS = 10
MAX_TIME_LIST = [2, 5, 10, 20, 50, 100, 200, 500]
PLAYERS_LIST = ['rand,bully,rdeep,ml']

def run_batch_experiments(repeats, max_time_list, players_list):
    i = 0

    print('🧪\tRunning a batch of experiments...')
    with progressbar.ProgressBar(max_value=(repeats*len(max_time_list)*len(players_list))) as bar:
        for max_time in max_time_list:
            for players in players_list:

                options.repeats = repeats
                options.max_time = max_time
                options.players = players

                run_experiment(options, is_batch = True)

                i += repeats
                bar.update(i)
    print('✨\tExperiments finished!')

if __name__ == "__main__":
    
    ## Parse the command line options
    parser = ArgumentParser()

    parser.add_argument("-b", "--batch",
                        dest="is_batch",
                        action="store_true",
                        help="Specify if you would like to run run_batch_experiments function")

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

    options = parser.parse_args()
    if options.is_batch:
        run_batch_experiments(REPEATS, MAX_TIME_LIST, PLAYERS_LIST)
    else:
        run_experiment(options)
