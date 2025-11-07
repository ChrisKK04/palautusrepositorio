import requests
from player import Player

class PlayerReader:
    def __init__(self, url):
        self.players_json = requests.get(url, timeout=10).json()

    def get_player(self, player):
        return Player(player)

    def get_players(self):
        return [Player(player) for player in self.players_json]
