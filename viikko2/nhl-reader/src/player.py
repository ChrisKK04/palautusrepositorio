class Player:
    def __init__(self, dictonary):
        self.name = dictonary['name']
        self.nationality = dictonary['nationality']
        self.assists = dictonary['assists']
        self.goals = dictonary['goals']
        self.points = self.goals + self.assists
        self.team = dictonary['team']
        self.games = dictonary['games']

    def name_and_nationality(self):
        return (self.name, self.nationality)

    def __str__(self):
        return (
            f"{self.name:20} team {self.team:15} "
            f"{self.goals:2} + {self.assists:2} = {self.points}"
        )
