def wins_to_csv(filename, bots_and_wins):
    bots, wins, avg_ms_move, times_late = bots_and_wins

    file_to_write = open(filename+'.csv', 'w')

    file_to_write.write(' , ')
    file_to_write.write((', ').join(map(lambda bot: bot+'_won', bots)) + '\n')

    for i in range(len(wins[0])):
        file_to_write.write(bots[i]+'_lost, ')
        file_to_write.write(
            ', '.join([str(bot_wins[i]) for bot_wins in wins]) + '\n')

    file_to_write.write('Total pts, ')
    file_to_write.write(', '.join(list(map(lambda list: str(sum(list)), wins))) + '\n')
    
    file_to_write.write('ms per move, ')
    file_to_write.write((', ').join(map(lambda x: str(x*1000)[:4], avg_ms_move)) + '\n')
    
    file_to_write.write('times late, ')
    file_to_write.write((', ').join(map(str, times_late)) + '\n')

    file_to_write.close()