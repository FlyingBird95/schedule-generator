from datetime import time
from typing import Dict, List, Tuple

import yaml

from .exceptions import ParseError
from .validators import validate_courts, validate_players, validate_teams
from ..models import Court, PlayerRegistry, Team
from ..api import teams_for_court, teams_for_player


def parse(filename) -> Tuple[List[Team], List[Court], PlayerRegistry]:
    """Read the contents from the YAML file."""
    try:
        with open(file=filename) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
    except Exception as e:
        raise ParseError(f"Cannot read the content of {filename}: {e}")
        
    courts = read_courts(data["courts"])
    court_by_name = {court.name: court for court in courts}
    teams, player_registry = read_teams(data["teams"], court_by_name=court_by_name)
    
    validate_courts(courts)
    validate_teams(teams, courts)
    validate_players(player_registry)
    
    return teams, courts, player_registry


def read_courts(data: List[Dict]) -> List[Court]:
    """Read the courts from the YAML file."""
    courts = []
    for item in data:
        begin_hour, begin_minute = item["begin"].split(":")
        end_hour, end_minute = item["end"].split(":")
        court = Court(
            name=item["name"],
            begin=time(hour=int(begin_hour), minute=int(begin_minute)),
            end=time(hour=int(end_hour), minute=int(end_minute)),
        )
        courts.append(court)
    return courts


def read_teams(data: List[Dict], court_by_name: Dict) -> Tuple[List[Team], PlayerRegistry]:
    """Read the teams from the YAML file."""
    teams = []
    player_registry = PlayerRegistry()
    
    for item in data:
        players = frozenset()
        if item["players"]:
            players = frozenset(player_registry.get_or_create(name) for name in item["players"])
        
        available_courts = frozenset()
        if item["availableCourts"]:
            try:
                available_courts = frozenset(court_by_name[name] for name in item["availableCourts"])
            except KeyError as e:
                [name] = e.args
                raise ParseError(f"Court {name} is not listed in courts. Please add this court and run again.")
        
        team = Team(
            name=item["name"],
            players=players,
            available_courts=available_courts,
        )
        
        # Add the team to the player
        for player in team.players:
            teams_for_player[player].add(team)
        
        # Add the team to the court
        for court in team.available_courts:
            teams_for_court[court].add(team)
        
        teams.append(team)
        
    return teams, player_registry
