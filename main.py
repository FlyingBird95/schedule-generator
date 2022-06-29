import logging
import sys
from argparse import ArgumentParser

from src.api import try_swap
from src.generate import get_initial_schedule
from src.input.exceptions import ParseError
from src.input.parsers import parse
from src.output.printer import print_players, print_schedule

logger = logging.getLogger("schedule")


def parse_args(arguments):
    parser = ArgumentParser(description="Generate a schedule given the input YAML file.")
    parser.add_argument("--filename", required=True, help="Input YAML file")
    return parser.parse_args(arguments)


def main():
    args = parse_args(sys.argv[1:])
    try:
        teams, courts, player_registry = parse(filename=args.filename)
    except ParseError as e:
        logger.error(e)
        return
    
    schedule = get_initial_schedule(teams=teams, courts=courts)
    if not schedule:
        logger.error(f"Initial schedule cannot be generated.")
        return

    print_schedule(schedule)
    for _ in range(10000):
        try_swap(schedule)
    
    print_schedule(schedule)


if __name__ == '__main__':
    main()
