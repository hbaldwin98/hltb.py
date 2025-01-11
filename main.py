from howlongtobeatpy import HowLongToBeat
from howlongtobeatpy.HowLongToBeatEntry import HowLongToBeatEntry
import time
import argparse
import logging

log_level = logging.INFO
logger = logging.getLogger(__name__)
verbose = False

def get_games(games, delay=1.0):
    results = [] 
    for game in games:
        results_list = HowLongToBeat().search(game)
        if results_list is not None and len(results_list) > 0:
            game = results_list[0]
            if verbose:
                logger.debug('FOUND: ' + game.game_name)
                if len(results_list) > 1:
                    logger.debug('MORE THAN ONE GAME FOUND:')
                    for result in results_list:
                        logger.debug('\t' + result.game_name)

            results.append(game)
        else:
            if verbose:
                logger.debug('NOT FOUND: %s', game)

            entry = HowLongToBeatEntry()
            entry.game_name = game

            results.append(entry)

        time.sleep(delay)

    return results

def to_csv(games, file_name='game_list.csv'):
    results = []
    results.append('title,main_story,main_extra,completionist,all_styles')

    for game in games:
        results.append('\n' + game.game_name + ',' + str(game.main_story) + ',' + str(game.main_extra) + ',' + str(game.completionist) + ',' + str(game.all_styles))

    if verbose:
        logger.debug('Start writing to file: %s', file_name)

    with open(file_name, 'w', encoding='utf-8') as f:
        f.writelines(results)
        f.close()

    if verbose:
        logger.debug('End writing to file: %s', file_name)

def main():
    global verbose, log_level

    parser = argparse.ArgumentParser(
        prog='HowLongToBeat Search',
        description='Searches HowLongToBeat for the results based on the input. Optional export',
        usage='python main.py "half life 2, bioshock" --delay 1 --filename output.csv --verbose --csv'
    )

    parser.add_argument('games')
    parser.add_argument('-d', '--delay')
    parser.add_argument('-c', '--csv', action=argparse.BooleanOptionalAction)
    parser.add_argument('-f', '--filename')
    parser.add_argument('-v', '--verbose', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    verbose = args.verbose

    if verbose:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
    logger.info('Starting...')

    game_strings = list(filter(lambda x: x is not None and len(x.strip()) != 0 , map(lambda x : x.strip(), args.games.strip().split(','))))
    delay = 1

    if args.delay is not None:
        try:
            delay = float(args.delay)
        except ValueError:
            logger.error('Invalid delay input must be a float: %s', args.delay)
            exit(1)

    games = get_games(game_strings, delay)

    if games is None or len(games) == 0:
        logger.debug('No games found.')
        exit(1)

    if args.csv:
        if args.filename is not None:
            to_csv(games, args.filename)
        else:
            to_csv(games)

    for game in games:
        logger.info('Games found:\n\nGame\t\t %s\nMain\t\t %s\nMain-Extra\t %s\nCompletionist\t %s\n',
            str(game.game_name),
            str(game.main_story),
            str(game.main_extra),
            str(game.completionist)
        )

    logger.info('Finished: ' + str(len(games)) + ' games')

if __name__ == '__main__':
    main()

