from dataclasses import dataclass, field
from datetime import time
from typing import Dict, FrozenSet, List

from src.configuration import SHOW_DEBUG_OUTPUT


@dataclass(frozen=True)
class Player:
    """Representation of a player."""
    name: str
    
    def __repr__(self):
        return self.name


@dataclass(frozen=True)
class Court:
    """Representation of a court in a moment in time."""
    name: str
    begin: time
    end: time
    
    def __repr__(self):
        return f"{self.name} ({self.begin} - {self.end})"
    
    def is_overlapping(self, other: "Court") -> bool:
        return self.begin < other.end and other.begin < self.end


@dataclass(frozen=True)
class Team:
    """Representation of a team."""
    name: str
    available_courts: FrozenSet[Court]
    players: FrozenSet[Player]
    
    def __repr__(self):
        return self.name


@dataclass
class Allocation:
    """Representation of a court assigned for a team."""
    court: Court
    team: Team


@dataclass
class Schedule:
    """Representation of a full schedule."""
    _allocations: List[Allocation] = field(default_factory=list)
    court_by_team: Dict[Team, Court] = field(default_factory=dict)
    
    def add(self, allocation):
        self._allocations.append(allocation)
        self.court_by_team[allocation.team] = allocation.court
    
    def swap(self, first_allocation: Allocation, second_allocation: Allocation):
        """Swap the two teams in the allocations and recompute several properties."""
        first_allocation.team, second_allocation.team = second_allocation.team, first_allocation.team
        self.court_by_team = {allocation.team: allocation.court for allocation in self._allocations}
    
    @property
    def teams(self) -> List[Team]:
        return [allocation.team for allocation in self._allocations]
    
    @property
    def courts(self) -> List[Court]:
        return [allocation.court for allocation in self._allocations]
    
    def can_add(self, allocation):
        """Returns true if the given allocation can be added to the list of allocations."""
        if allocation.team in self.teams:
            return False
        
        if allocation.court in self.courts:
            return False
        
        return True
    
    def is_valid(self) -> bool:
        from src.api import teams_for_player
        
        for team, court in self.court_by_team.items():
            for player in team.players:
                teams = teams_for_player[player]
                for other_team in teams:
                    if other_team == team:
                        continue  # skip comparing own team
                    other_court = self.court_by_team[other_team]
                    if court.is_overlapping(other_court):
                        return False
        return True


@dataclass
class PlayerRegistry:
    """Helper class to retrieve a Player object by name."""
    _players_by_name: Dict[str, Player] = field(default_factory=dict)
    
    @property
    def players(self):
        """Return the players in a list sorted alphabetically by name."""
        return list(sorted(self._players_by_name.values(), key=lambda p: p.name))
    
    def get_or_create(self, name) -> Player:
        """Creates the player if it doesn't exist."""
        if name not in self._players_by_name:
            self._players_by_name[name] = Player(name=name)
        return self._players_by_name[name]
