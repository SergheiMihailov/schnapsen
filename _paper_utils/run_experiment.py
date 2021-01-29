#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import progressbar
import pickle

sys.path.append(os.path.realpath('.'))

from tournament import run_tournament
from argparse import ArgumentParser
from output_formatters import result_to_csv, result_summary_to_csv

def run_experiment(options, is_batch = False, specific_bot_to_test=None):
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
    
    result_to_csv(filename, result)

    if not is_batch: print('✨\tExperiment finished!  \n\tData saved in '+filename)

    return result

REPEATS = 1000
MAX_TIME_LIST = [1, 2, 5, 10, 20, 50, 100, 200]
PLAYERS_LIST = ['selection_basic,selection_weighted_probability']

def run_batch_experiments(repeats, max_time_list, players_list):
    i = 0

    print('🧪\tRunning a batch of experiments...')
    result_summary = {}
    with progressbar.ProgressBar(max_value=repeats*len(max_time_list)*len(players_list)) as bar:
        for max_time in max_time_list:
            for players in players_list:

                options.repeats = repeats
                options.max_time = max_time
                options.players = players

                bot_names, scores, ms_per_move, times_late = run_experiment(options, is_batch = True)
                
                result = {'bot_names': bot_names, 'scores': scores, 'ms_per_move': ms_per_move, 'times_late': times_late}

                result_summary[max_time] = result

                i += repeats
                bar.update(i)

    summary_filename =  os.path.realpath('_paper_utils/result_summary/summary_reps-' + str(options.repeats)+'_players-'+options.players)
    summary_filename_pkl = summary_filename+'.pkl'
    
    open(summary_filename_pkl, 'w').write(pickle.dumps(result_summary))
    
    result_summary_to_csv(summary_filename, result_summary)

    print('✨\tExperiments finished! \n\tSummary data saved in '+summary_filename)

def summarize_results():
    
    result_summary = {}

    for max_time in MAX_TIME_LIST:
        filename =  os.path.realpath('_paper_utils/results/reps-' + str(REPEATS) + '_time-'+str(max_time)+'_players-'+','.join(PLAYERS_LIST ))
        filename_pkl = filename+'.pkl'
    
        file = open(filename_pkl, 'r')

        bot_names, scores, ms_per_move, times_late = pickle.load(file)
        total_scores = [0]*len(scores)
        for i in range(len(scores)):
            total_scores[i] += sum(scores[i])
        result = {'bot_names': bot_names, 'scores': total_scores, 'ms_per_move': ms_per_move, 'times_late': times_late}
    
        result_summary[max_time] = result
    
    summary_filename =  os.path.realpath('_paper_utils/result_summary/summary_reps-' +  str(REPEATS)+'_players-'+','.join(PLAYERS_LIST ))
    summary_filename_pkl = summary_filename+'.pkl'

    open(summary_filename_pkl, 'w').write(pickle.dumps(result_summary))
    
    result_summary_to_csv(summary_filename, result_summary)


if __name__ == "__main__":
    
    ## Parse the command line options
    parser = ArgumentParser()

    parser.add_argument("-b", "--batch",
                        dest="is_batch",
                        action="store_true",
                        help="Specify if you would like to run run_batch_experiments function")

    parser.add_argument("-s", "--summarize",
                        dest="is_summarize",
                        action="store_true",
                        help="Specify if you would like to run summarize-results function")

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
    elif options.is_summarize:
        summarize_results()
    else:
        run_experiment(options)
