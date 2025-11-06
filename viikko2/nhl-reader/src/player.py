class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.assists = dict['assists']
        self.goals = dict['goals']
        self.team = dict['team']
        self.games = dict['games']
        self.id = dict['id']
    
    def __str__(self):
        return f"{self.name:20} team {self.team:15} {self.goals:2} + {self.assists:2} = {self.goals + self.assists}"


# {"name":"Max Crozier","nationality":"CAN","assists":0,"goals":0,"team":"TBL","games":5,"id":8481719}