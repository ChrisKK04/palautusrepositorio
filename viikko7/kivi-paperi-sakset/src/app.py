from flask import Flask, render_template, request, jsonify
from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
import os
import uuid

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# Game configuration - change this value to set rounds needed to win
ROUNDS_TO_WIN = 5

# Store game states in memory
game_states = {}


class WebGameState:
    def __init__(self, game_type, rounds_to_win=ROUNDS_TO_WIN):
        self.game_type = game_type
        self.tuomari = Tuomari()
        self.rounds_to_win = rounds_to_win
        self.game_finished = False
        self.winner = None
        
        if game_type == 'simple_ai':
            self.ai = Tekoaly()
        elif game_type == 'advanced_ai':
            self.ai = TekoalyParannettu(10)
        else:
            self.ai = None
        
        # For PvP mode
        self.player1_move = None
        self.player2_move = None
        self.current_turn = 1  # 1 for player 1, 2 for player 2
    
    def is_valid_move(self, move):
        return move in ['k', 'p', 's']
    
    def get_ai_move(self):
        if self.ai is None:
            return None
        return self.ai.anna_siirto()
    
    def record_ai_move(self, player_move):
        if self.ai is None:
            return
        if isinstance(self.ai, TekoalyParannettu):
            self.ai.aseta_siirto(player_move)
    
    def play_round(self, player1_move, player2_move):
        if not (self.is_valid_move(player1_move) and self.is_valid_move(player2_move)):
            return None
        
        if self.game_finished:
            return None
        
        self.tuomari.kirjaa_siirto(player1_move, player2_move)
        
        # Check if game is finished
        if self.tuomari.ekan_pisteet >= self.rounds_to_win:
            self.game_finished = True
            self.winner = 1
        elif self.tuomari.tokan_pisteet >= self.rounds_to_win:
            self.game_finished = True
            self.winner = 2
        
        return {
            'player1_move': self.translate_move(player1_move),
            'player2_move': self.translate_move(player2_move),
            'player1_score': self.tuomari.ekan_pisteet,
            'player2_score': self.tuomari.tokan_pisteet,
            'draws': self.tuomari.tasapelit,
            'game_finished': self.game_finished,
            'winner': self.winner
        }
    
    def translate_move(self, move):
        if move == 'k':
            return 'Kivi'
        elif move == 'p':
            return 'Paperi'
        elif move == 's':
            return 'Sakset'
        return move
    
    def get_result(self):
        return {
            'player1_score': self.tuomari.ekan_pisteet,
            'player2_score': self.tuomari.tokan_pisteet,
            'draws': self.tuomari.tasapelit,
            'game_finished': self.game_finished,
            'winner': self.winner,
            'rounds_to_win': self.rounds_to_win
        }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.json
    game_type = data.get('game_type', 'pvp')
    
    # Create new game
    game_id = str(uuid.uuid4())
    game_state = WebGameState(game_type)
    game_states[game_id] = game_state
    
    player2_name = 'Pelaaja 2'
    if game_type == 'simple_ai':
        player2_name = 'Tekoäly (yksinkertainen)'
    elif game_type == 'advanced_ai':
        player2_name = 'Tekoäly (parannettu)'
    
    return jsonify({
        'success': True,
        'game_id': game_id,
        'player2_name': player2_name,
        'rounds_to_win': ROUNDS_TO_WIN
    })


@app.route('/api/play_round', methods=['POST'])
def play_round():
    data = request.json
    game_id = data.get('game_id')
    player_move = data.get('move')
    
    if game_id not in game_states:
        return jsonify({'error': 'Game not found'}), 400
    
    game_state = game_states[game_id]
    
    if game_state.game_finished:
        return jsonify({'error': 'Game already finished'}), 400
    
    if not game_state.is_valid_move(player_move):
        return jsonify({'error': 'Invalid move'}), 400
    
    # Handle PvP mode
    if game_state.game_type == 'pvp':
        if game_state.current_turn == 1:
            # Player 1 makes a move
            game_state.player1_move = player_move
            game_state.current_turn = 2
            return jsonify({
                'success': True,
                'message': 'Player 1 move recorded. Waiting for Player 2.',
                'next_player': 2
            })
        else:
            # Player 2 makes a move
            game_state.player2_move = player_move
            
            # Both players have moved, play the round
            result = game_state.play_round(game_state.player1_move, game_state.player2_move)
            
            # Reset for next round
            game_state.player1_move = None
            game_state.player2_move = None
            game_state.current_turn = 1
            
            return jsonify(result)
    else:
        # AI mode
        player1_move = player_move
        player2_move = game_state.get_ai_move()
        game_state.record_ai_move(player1_move)
        
        result = game_state.play_round(player1_move, player2_move)
        
        if result is None:
            return jsonify({'error': 'Invalid move'}), 400
        
        return jsonify(result)


@app.route('/api/get_state', methods=['GET'])
def get_state():
    game_id = request.args.get('game_id')
    
    if game_id not in game_states:
        return jsonify({'error': 'Game not found'}), 400
    
    game_state = game_states[game_id]
    
    return jsonify(game_state.get_result())


if __name__ == '__main__':
    app.run(debug=True, port=5000)
