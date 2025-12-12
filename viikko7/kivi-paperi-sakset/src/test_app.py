import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, WebGameState, game_states


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
        
    def test_init_advanced_ai(self):
        game = WebGameState('advanced_ai')
        assert game.game_type == 'advanced_ai'
        assert game.ai is not None
        
    def test_init_pvp(self):
        game = WebGameState('pvp')
        assert game.game_type == 'pvp'
        assert game.ai is None
        assert game.player1_move is None
        assert game.player2_move is None
        assert game.current_turn == 1
        
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
        
    def test_play_round_player1_wins(self):
        game = WebGameState('simple_ai')
        result = game.play_round('k', 's')  # Rock beats Scissors
        assert result['player1_score'] == 1
        assert result['player2_score'] == 0
        assert result['draws'] == 0
        
    def test_play_round_player2_wins(self):
        game = WebGameState('simple_ai')
        result = game.play_round('s', 'k')  # Scissors loses to Rock
        assert result['player1_score'] == 0
        assert result['player2_score'] == 1
        assert result['draws'] == 0


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
        
    def test_start_game_advanced_ai(self, client):
        response = client.post('/api/start_game',
                              json={'game_type': 'advanced_ai'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert data['player2_name'] == 'Tekoäly (parannettu)'
        
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


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
