import random
from collections import defaultdict
from datetime import time
from typing import Dict, Set

from .models import Court, Player, Schedule, Team

teams_for_player: Dict[Player, Set[Team]] = defaultdict(set)
"""Global helper dict to store in which teams a player is involved."""

teams_for_court: Dict[Court, Set[Team]] = defaultdict(set)
"""Global helper dict to store in which teams a court is involved."""


def get_other_teams_for_player(player: Player, current_team: Team) -> Set[Team]:
    """Get the other teams for the player."""
    return {team for team in teams_for_player[player] if team != current_team}


def get_minutes(time_object: time) -> int:
    return time_object.hour * 60 + time_object.minute


def get_waiting_time(schedule: Schedule, with_print=False) -> int:
    total = 0
    for team in schedule.teams:
        for player in team.players:
            other_teams = get_other_teams_for_player(player, current_team=team)
            if not other_teams:
                continue
            applicable_courts = [schedule.court_by_team[t] for t in other_teams]
            applicable_courts.append(schedule.court_by_team[team])
            
            first_court = min(applicable_courts, key=lambda item: item.begin)
            last_court = max(applicable_courts, key=lambda item: item.end)
            waiting_time = get_minutes(last_court.begin) - get_minutes(first_court.end)
            if with_print and waiting_time:
                print(f"Player {player} needs to wait {waiting_time}: '{first_court.end}' - '{last_court.begin}'.")
            total += waiting_time
    
    return total // 2


def try_swap(schedule: Schedule):
    current_waiting_time = get_waiting_time(schedule)
    
    first, second = random.choices(schedule._allocations, k=2)
    schedule.swap(first, second)
    
    if not schedule.is_valid():
        schedule.swap(first, second)  # not valid, swap back
    
    new_waiting_time = get_waiting_time(schedule)
    if new_waiting_time > current_waiting_time:
        schedule.swap(first, second)  # bad move, swap back
