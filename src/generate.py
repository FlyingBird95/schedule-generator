from random import shuffle
from typing import List, Optional

from .models import Allocation, Court, Schedule, Team
from .api import teams_for_player

MAX_ITERATIONS = 500000


def try_selection(courts_shuffled: List[Court], teams: List[Team]) -> Optional[Schedule]:
    schedule = Schedule()
    
    for team, court in zip(teams, courts_shuffled):
        if court not in team.available_courts:
            return
        allocation = Allocation(court=court, team=team)
        if not schedule.can_add(allocation):
            return
        
        schedule.add(allocation)
    
    if not schedule.is_valid():
        return
    
    return schedule


def get_initial_schedule(courts: List[Court], teams: List[Team]):
    for _ in range(MAX_ITERATIONS):
        courts_shuffled = courts[:]  # copy the list of courts
        shuffle(courts_shuffled)
        schedule = try_selection(courts_shuffled=courts_shuffled, teams=teams)
        if schedule is not None:
            return schedule
