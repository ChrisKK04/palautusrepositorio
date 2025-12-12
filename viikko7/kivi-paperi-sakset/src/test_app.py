import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, WebGameState, game_states, ROUNDS_TO_WIN
from tekoaly_elite import TekoalyElite


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    # Clean up game states after each test
    game_states.clear()


class TestWebGameState:
    """Test the WebGameState class."""
    
    def test_init_simple_ai(self):
        game = WebGameState('simple_ai')
        assert game.game_type == 'simple_ai'
        assert game.ai is not None
        assert game.tuomari is not None
        assert game.game_finished == False
        assert game.winner is None
        assert game.rounds_to_win == ROUNDS_TO_WIN
        
    def test_init_advanced_ai(self):
        game = WebGameState('advanced_ai')
        assert game.game_type == 'advanced_ai'
        assert game.ai is not None
        assert game.game_finished == False
        
    def test_init_elite_ai(self):
        game = WebGameState('elite_ai')
        assert game.game_type == 'elite_ai'
        assert game.ai is not None
        assert isinstance(game.ai, TekoalyElite)
        assert game.game_finished == False
        
    def test_init_pvp(self):
        game = WebGameState('pvp')
        assert game.game_type == 'pvp'
        assert game.ai is None
        assert game.player1_move is None
        assert game.player2_move is None
        assert game.current_turn == 1
        assert game.game_finished == False
        
    def test_is_valid_move(self):
        game = WebGameState('simple_ai')
        assert game.is_valid_move('k') == True
        assert game.is_valid_move('p') == True
        assert game.is_valid_move('s') == True
        assert game.is_valid_move('x') == False
        assert game.is_valid_move('') == False
        
    def test_translate_move(self):
        game = WebGameState('simple_ai')
        assert game.translate_move('k') == 'Kivi'
        assert game.translate_move('p') == 'Paperi'
        assert game.translate_move('s') == 'Sakset'
        
    def test_play_round_draw(self):
        game = WebGameState('simple_ai')
        result = game.play_round('k', 'k')
        assert result['player1_move'] == 'Kivi'
        assert result['player2_move'] == 'Kivi'
        assert result['draws'] == 1
        assert result['player1_score'] == 0
        assert result['player2_score'] == 0
        assert result['game_finished'] == False
        assert result['winner'] is None
        
    def test_play_round_player1_wins(self):
        game = WebGameState('simple_ai')
        result = game.play_round('k', 's')  # Rock beats Scissors
        assert result['player1_score'] == 1
        assert result['player2_score'] == 0
        assert result['draws'] == 0
        assert result['game_finished'] == False
        
    def test_play_round_player2_wins(self):
        game = WebGameState('simple_ai')
        result = game.play_round('s', 'k')  # Scissors loses to Rock
        assert result['player1_score'] == 0
        assert result['player2_score'] == 1
        assert result['draws'] == 0
        assert result['game_finished'] == False
    
    def test_game_ends_when_player1_wins_enough_rounds(self):
        game = WebGameState('simple_ai', rounds_to_win=3)
        # Play rounds until player 1 wins 3
        for _ in range(3):
            result = game.play_round('k', 's')
        assert result['game_finished'] == True
        assert result['winner'] == 1
        assert result['player1_score'] == 3
        
    def test_game_ends_when_player2_wins_enough_rounds(self):
        game = WebGameState('simple_ai', rounds_to_win=3)
        # Play rounds until player 2 wins 3
        for _ in range(3):
            result = game.play_round('s', 'k')
        assert result['game_finished'] == True
        assert result['winner'] == 2
        assert result['player2_score'] == 3
        
    def test_cannot_play_after_game_finished(self):
        game = WebGameState('simple_ai', rounds_to_win=2)
        # Play until game ends
        game.play_round('k', 's')
        game.play_round('k', 's')
        assert game.game_finished == True
        # Try to play another round
        result = game.play_round('k', 's')
        assert result is None


class TestFlaskRoutes:
    """Test Flask API endpoints."""
    
    def test_index_route(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi, Paperi, Sakset' in response.data
        
    def test_start_game_simple_ai(self, client):
        response = client.post('/api/start_game',
                              json={'game_type': 'simple_ai'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'game_id' in data
        assert data['player2_name'] == 'Tekoäly (yksinkertainen)'
        assert data['rounds_to_win'] == ROUNDS_TO_WIN
        
    def test_start_game_advanced_ai(self, client):
        response = client.post('/api/start_game',
                              json={'game_type': 'advanced_ai'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert data['player2_name'] == 'Tekoäly (parannettu)'
        
    def test_start_game_elite_ai(self, client):
        response = client.post('/api/start_game',
                              json={'game_type': 'elite_ai'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert data['player2_name'] == 'Tekoäly (Elite)'
        
    def test_start_game_pvp(self, client):
        response = client.post('/api/start_game',
                              json={'game_type': 'pvp'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert data['player2_name'] == 'Pelaaja 2'
        
    def test_play_round_ai_mode(self, client):
        # Start a game
        start_response = client.post('/api/start_game',
                                    json={'game_type': 'simple_ai'})
        game_id = start_response.get_json()['game_id']
        
        # Play a round
        response = client.post('/api/play_round',
                              json={'game_id': game_id, 'move': 'k'})
        assert response.status_code == 200
        data = response.get_json()
        assert 'player1_move' in data
        assert 'player2_move' in data
        assert 'player1_score' in data
        assert 'player2_score' in data
        assert 'draws' in data
        
    def test_play_round_elite_ai_mode(self, client):
        # Start elite AI game
        start_response = client.post('/api/start_game',
                                    json={'game_type': 'elite_ai'})
        game_id = start_response.get_json()['game_id']
        
        # Play multiple rounds
        for _ in range(3):
            response = client.post('/api/play_round',
                                  json={'game_id': game_id, 'move': 'k'})
            assert response.status_code == 200
            data = response.get_json()
            assert 'player1_move' in data
            assert 'player2_move' in data
        
    def test_play_round_invalid_game_id(self, client):
        response = client.post('/api/play_round',
                              json={'game_id': 'invalid-id', 'move': 'k'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        
    def test_play_round_invalid_move(self, client):
        # Start a game
        start_response = client.post('/api/start_game',
                                    json={'game_type': 'simple_ai'})
        game_id = start_response.get_json()['game_id']
        
        # Try invalid move
        response = client.post('/api/play_round',
                              json={'game_id': game_id, 'move': 'x'})
        assert response.status_code == 400
        
    def test_pvp_mode_flow(self, client):
        # Start PvP game
        start_response = client.post('/api/start_game',
                                    json={'game_type': 'pvp'})
        game_id = start_response.get_json()['game_id']
        
        # Player 1 makes a move
        response1 = client.post('/api/play_round',
                               json={'game_id': game_id, 'move': 'k'})
        assert response1.status_code == 200
        data1 = response1.get_json()
        assert data1['next_player'] == 2
        assert data1['success'] == True
        
        # Player 2 makes a move
        response2 = client.post('/api/play_round',
                               json={'game_id': game_id, 'move': 'p'})
        assert response2.status_code == 200
        data2 = response2.get_json()
        assert 'player1_move' in data2
        assert 'player2_move' in data2
        assert data2['player1_move'] == 'Kivi'
        assert data2['player2_move'] == 'Paperi'
        assert data2['player2_score'] == 1  # Paper beats Rock
        
    def test_get_state(self, client):
        # Start a game
        start_response = client.post('/api/start_game',
                                    json={'game_type': 'simple_ai'})
        game_id = start_response.get_json()['game_id']
        
        # Play a round
        client.post('/api/play_round',
                   json={'game_id': game_id, 'move': 'k'})
        
        # Get state
        response = client.get(f'/api/get_state?game_id={game_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert 'player1_score' in data
        assert 'player2_score' in data
        assert 'draws' in data
        assert 'game_finished' in data
        assert 'winner' in data
        assert 'rounds_to_win' in data
        
    def test_get_state_invalid_game(self, client):
        response = client.get('/api/get_state?game_id=invalid-id')
        assert response.status_code == 400
        
    def test_multiple_rounds(self, client):
        # Start a game
        start_response = client.post('/api/start_game',
                                    json={'game_type': 'simple_ai'})
        game_id = start_response.get_json()['game_id']
        
        # Play multiple rounds
        for move in ['k', 'p', 's']:
            response = client.post('/api/play_round',
                                  json={'game_id': game_id, 'move': move})
            assert response.status_code == 200
            
        # Verify state has been updated
        state_response = client.get(f'/api/get_state?game_id={game_id}')
        data = state_response.get_json()
        total_rounds = data['player1_score'] + data['player2_score'] + data['draws']
        assert total_rounds == 3
    
    def test_game_ends_after_winning_rounds(self, client):
        # Start a game
        start_response = client.post('/api/start_game',
                                    json={'game_type': 'simple_ai'})
        game_id = start_response.get_json()['game_id']
        
        # Play enough rounds to win (ROUNDS_TO_WIN rounds where player 1 wins)
        # We need to know AI pattern: starts with 'p', then 's', then 'k', repeats
        # So to win, we play: s (beats p), k (beats s), p (beats k), repeat
        winning_moves = ['s', 'k', 'p'] * ((ROUNDS_TO_WIN // 3) + 2)
        
        last_response = None
        for i, move in enumerate(winning_moves[:ROUNDS_TO_WIN]):
            response = client.post('/api/play_round',
                                  json={'game_id': game_id, 'move': move})
            last_response = response
            if response.status_code != 200:
                break
                
        # Check that game finished
        data = last_response.get_json()
        assert data['game_finished'] == True
        assert data['winner'] == 1
        
        # Try to play another round - should fail
        response = client.post('/api/play_round',
                             json={'game_id': game_id, 'move': 'k'})
        assert response.status_code == 400


class TestTekoalyElite:
    """Test the TekoalyElite AI class."""
    
    def test_init(self):
        ai = TekoalyElite(100)
        assert ai._history == []
        assert ai._ai_history == []
        assert ai._history_size == 100
    
    def test_counter_moves(self):
        ai = TekoalyElite()
        assert ai._counter('k') == 'p'
        assert ai._counter('p') == 's'
        assert ai._counter('s') == 'k'
    
    def test_beats_logic(self):
        ai = TekoalyElite()
        assert ai._beats('k', 's') == True
        assert ai._beats('p', 'k') == True
        assert ai._beats('s', 'p') == True
        assert ai._beats('k', 'p') == False
        assert ai._beats('p', 's') == False
        assert ai._beats('s', 'k') == False
        assert ai._beats('k', 'k') == False
    
    def test_records_opponent_moves(self):
        ai = TekoalyElite(10)
        ai.aseta_siirto('k')
        ai.aseta_siirto('p')
        ai.aseta_siirto('s')
        
        assert ai._history == ['k', 'p', 's']
    
    def test_history_bounded(self):
        ai = TekoalyElite(3)
        for i in range(5):
            ai.aseta_siirto('k')
        
        # History should only keep last 3 items
        assert len(ai._history) == 3
    
    def test_generates_valid_move(self):
        ai = TekoalyElite()
        move = ai.anna_siirto()
        assert move in ['k', 'p', 's']
    
    def test_frequency_analysis(self):
        """Test that elite AI counters most frequent move."""
        ai = TekoalyElite()
        # Opponent mostly plays rock
        for _ in range(5):
            ai.aseta_siirto('k')
        ai.aseta_siirto('p')
        ai.aseta_siirto('s')
        
        prediction = ai._frequency_analysis()
        assert prediction == 'p'  # Should counter rock with paper
    
    def test_pattern_detection(self):
        """Test pattern matching in opponent moves."""
        ai = TekoalyElite()
        # Create a repeating pattern
        pattern = ['k', 'p', 's']
        ai._history = pattern + pattern + ['k']
        
        next_move = ai._find_sequence_pattern(ai._history)
        assert next_move is not None


class TestEliteAIIntegration:
    """Test elite AI in game context."""
    
    def test_elite_ai_game_state(self):
        game = WebGameState('elite_ai')
        assert game.ai is not None
        assert isinstance(game.ai, TekoalyElite)
        
        # Play several rounds
        for _ in range(5):
            ai_move = game.get_ai_move()
            player_move = 'k'
            game.record_ai_move(player_move)
            
            assert ai_move in ['k', 'p', 's']
    
    def test_elite_ai_learns_from_patterns(self):
        game = WebGameState('elite_ai')
        
        # Play multiple rock moves
        for _ in range(3):
            game.record_ai_move('k')
        
        # AI should counter with paper
        ai_move = game.get_ai_move()
        assert ai_move == 'p'  # Counters rock with paper


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
