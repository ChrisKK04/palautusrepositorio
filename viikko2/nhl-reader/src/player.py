class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.assists = dict['assists']
        self.goals = dict['goals']
        self.points = self.goals + self.assists
        self.team = dict['team']
        self.games = dict['games']
        self.id = dict['id']
    
    def __str__(self):
        return f"{self.name:20} team {self.team:15} {self.goals:2} + {self.assists:2} = {self.points}"