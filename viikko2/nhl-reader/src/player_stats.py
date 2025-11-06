class PlayerStats:

    def __init__(self, players):
        self.players = players

    def top_scorers_by_nationality(self, country):
        sorted_players = sorted(
            [player for player in self.players if player.nationality == country], # removing other nationalities
            reverse=True, # highest points first
            key=lambda player: player.assists + player.goals # sorting by points
        )

        return sorted_players