import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
    
    def test_pelaaja_haku(self):
        self.assertEqual(str(self.stats.search("Semenko")), "Semenko EDM 4 + 12 = 16")

    def test_pelaaja_haku_ei_ole(self):
        self.assertEqual(str(self.stats.search("Simon")), "None")

    def test_tiimi_haku(self):
        team_list = []
        team = self.stats.team("EDM")
        for player in team:
            team_list.append(str(player))

        self.assertEqual(team_list, ['Semenko EDM 4 + 12 = 16',
                                     'Kurri EDM 37 + 53 = 90',
                                     'Gretzky EDM 35 + 89 = 124'])
    
    def test_top_pisteet(self):
        top_players = []
        top = self.stats.top(2)
        for player in top:
            top_players.append(str(player))

        self.assertEqual(top_players, ['Gretzky EDM 35 + 89 = 124',
                                       'Lemieux PIT 45 + 54 = 99',
                                       'Yzerman DET 42 + 56 = 98'])
        
    def test_top_maalit(self):
        top_players = []
        top = self.stats.top(2, SortBy.GOALS)
        for player in top:
            top_players.append(str(player))

        self.assertEqual(top_players, ['Lemieux PIT 45 + 54 = 99',
                                       'Yzerman DET 42 + 56 = 98',
                                       'Kurri EDM 37 + 53 = 90'])
        
    def test_top_syotot(self):
        top_players = []
        top = self.stats.top(2, SortBy.ASSISTS)
        for player in top:
            top_players.append(str(player))

        self.assertEqual(top_players, ['Gretzky EDM 35 + 89 = 124',
                                       'Yzerman DET 42 + 56 = 98',
                                       'Lemieux PIT 45 + 54 = 99'])