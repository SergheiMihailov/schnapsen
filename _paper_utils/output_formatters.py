def result_to_csv(filename, result):
    bot_names, scores, ms_per_move, times_late = result

    file_to_write = open(filename+'.csv', 'w')

    file_to_write.write(' , ')
    file_to_write.write((', ').join(map(lambda bot: bot+'_won', bot_names)) + '\n')

    for i in range(len(scores[0])):
        file_to_write.write(bot_names[i]+'_lost, ')
        file_to_write.write(
            ', '.join([str(bot_score[i]) for bot_score in scores]) + '\n')

    file_to_write.write('Total pts, ')
    file_to_write.write(', '.join(list(map(lambda list: str(sum(list)), scores))) + '\n')
    
    file_to_write.write('ms per move, ')
    file_to_write.write((', ').join(map(lambda x: str(x*1000)[:4], ms_per_move)) + '\n')
    
    file_to_write.write('times late, ')
    file_to_write.write((', ').join(map(str, times_late)) + '\n')

    file_to_write.close()

def result_summary_to_csv(summary_filename, result_summary):
    file_to_write = open(summary_filename+'.csv', 'w')
    file_to_write.write('max_time, bot_name, score, ms_per_move, times_late\n')

    for max_time in sorted(result_summary.keys()):
        for i in range(len(result_summary[max_time]['bot_names'])):
            data_to_write = ', '.join(map(
                    lambda entry: str(entry), 
                    [ 
                        max_time, 
                        result_summary[max_time]['bot_names'][i], 
                        result_summary[max_time]['scores'][i],
                        result_summary[max_time]['ms_per_move'][i], 
                        result_summary[max_time]['times_late'][i]
                    ]
                )) + '\n'
            file_to_write.write(data_to_write)
                

    file_to_write.close()