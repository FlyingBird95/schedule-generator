from typing import List

from ..models import Player, Schedule
from ..api import get_waiting_time, teams_for_player


def print_players(players: List[Player]):
    print("\n\n- - - PLAYERS - - -")
    for player in players:
        team_names = ", ".join(repr(team) for team in teams_for_player[player])
        print(f"Player {player} is involved in: {team_names}")


def print_schedule(schedule: Schedule):
    print("\n\n- - - SCHEDULE - - -")
    for team, court in sorted(schedule.court_by_team.items(), key=lambda item: item[1].begin):
        print(f"Court {court} has been allocated for {team}")
    
    print(f"\nTotal waiting time: {get_waiting_time(schedule, with_print=True)} minutes")
