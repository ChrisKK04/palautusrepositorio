class TennisGame:
    LEADER_PLAYER1 = 1
    LEADER_PLAYER2 = -1
    WINNER_PLAYER1 = 2

    END_CLOSE = 4

    ADVANTAGE = "Advantage"
    WIN_FOR = "Win for"
    DEUCE = "Deuce"

    POINTS_EVEN = {
        0: "Love-All",
        1: "Fifteen-All",
        2: "Thirty-All"
    }

    POINTS = {
        0: "Love",
        1: "Fifteen",
        2: "Thirty",
        3: "Forty"
    }

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.m_score1 += 1
        else:
            self.m_score2 += 1

    def get_score(self):
        if self.m_score1 == self.m_score2:
            score = self._score_even(self.m_score1)

        elif self.m_score1 >= self.END_CLOSE or self.m_score2 >= self.END_CLOSE:
            score = self._score_lead(self.m_score1, self.m_score2)
        
        else:
            score = self._score_normal(self.m_score1, self.m_score2)

        return score
    
    def _score_even(self, score):
        return self.POINTS_EVEN.get(score, self.DEUCE)

    def _score_lead(self, score1, score2):
        difference = score1 - score2
        if difference == self.LEADER_PLAYER1:
            score = f"{self.ADVANTAGE} {self.player1_name}"
        elif difference == self.LEADER_PLAYER2:
            score = f"{self.ADVANTAGE} {self.player2_name}"
        elif difference >= self.WINNER_PLAYER1:
            score = f"{self.WIN_FOR} {self.player1_name}"
        else:
            score = f"{self.WIN_FOR} {self.player2_name}"

        return score

    def _score_normal(self, score1, score2):
        return f"{self.POINTS[score1]}-{self.POINTS[score2]}"
