import logging
from collections import Counter
from typing import List

from .exceptions import ParseError
from ..models import Court, PlayerRegistry, Team
from ..api import teams_for_court, teams_for_player

logger = logging.getLogger("schedule")


def validate_courts(courts: List[Court]):
    """Validate all courts have unique names."""
    counter = Counter(court.name for court in courts)
    for value, occurrence in counter.items():
        if occurrence > 1:
            raise ParseError(f"Not all court names are unique: {value}.")
    
    for court in courts:
        if not teams_for_court[court]:
            raise ParseError(f"Court {court} has no available teams.")


def validate_players(player_registry: PlayerRegistry):
    """Validate players against the number of teams."""
    for player in player_registry.players:
        teams = teams_for_player[player]
        if len(teams) < 2:
            team_names = ", ".join(team.name for team in teams)
            logger.warning(
                f"Player {player} occurs in less than two teams: {team_names}. This player will never "
                f"cause conflicts so you can remove it from the input data."
            )


def validate_teams(teams: List[Team], courts: List[Court]):
    """Validate that there are more/equal courts then teams."""
    if len(courts) < len(teams):
        raise ParseError(
            f"No schedule can be generated, because there are {len(courts)} courts for {len(teams)} teams."
        )
