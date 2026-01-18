from dataclasses import dataclass

@dataclass
class Team:
    id:int
    year: int
    team_code:int
    name:str

    def __str__(self):
        return f'{self.id} ({self.year}) {self.team_code} {self.name}'

    def __repr__(self):
        return f'{self.id} ({self.year}) {self.team_code} {self.name}'

    def __hash__(self):
        return hash(self.id)

