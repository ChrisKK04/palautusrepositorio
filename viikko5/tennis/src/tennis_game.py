class TennisGame:
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2

    LEADER_PLAYER1 = 1
    LEADER_PLAYER2 = -1
    WINNDER_PLAYER1 = 2

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.m_score1 = self.m_score1 + 1
        else:
            self.m_score2 = self.m_score2 + 1

    def get_score(self):
        score = ""
        temp_score = 0

        if self.m_score1 == self.m_score2:
            return self._score_even(self.m_score1)

        elif self.m_score1 >= 4 or self.m_score2 >= 4:
            return self._score_lead(self.m_score1, self.m_score2)

        else:
            for i in range(1, 3):
                if i == 1:
                    temp_score = self.m_score1
                else:
                    score = score + "-"
                    temp_score = self.m_score2

                if temp_score == 0:
                    score = score + "Love"
                elif temp_score == 1:
                    score = score + "Fifteen"
                elif temp_score == 2:
                    score = score + "Thirty"
                elif temp_score == 3:
                    score = score + "Forty"

        return score
    
    def _score_even(self, score):
        if score == self.LOVE:
            score = "Love-All"
        elif score == self.FIFTEEN:
            score = "Fifteen-All"
        elif score == self.THIRTY:
            score = "Thirty-All"
        else:
            score = "Deuce"

        return score

    def _score_lead(self, score1, score2):
        difference = score1 - score2
        if difference == self.LEADER_PLAYER1:
            score = "Advantage player1"
        elif difference == self.LEADER_PLAYER2:
            score = "Advantage player2"
        elif difference >= self.WINNDER_PLAYER1:
            score = "Win for player1"
        else:
            score = "Win for player2"

        return score
