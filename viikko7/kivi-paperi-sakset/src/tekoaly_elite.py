import random


class TekoalyElite:
    """
    Elite AI inspired by Iocaine Powder (International RPS Programming Contest winner 1999).
    
    Uses multiple strategies with metastrategies:
    1. History matching - detects patterns in opponent's move sequences
    2. Frequency analysis - exploits bias towards certain moves
    3. Adaptive counter-strategies - predicts and counters the opponent's strategy
    4. Random fallback - prevents predictability
    
    The AI learns opponent patterns and adapts dynamically.
    """
    
    def __init__(self, history_size=100):
        self._history = []  # List of opponent moves
        self._ai_history = []  # List of AI's own moves
        self._history_size = history_size
        self._strategy_scores = {
            'history_match': 0,
            'frequency': 0,
            'random': 0
        }
        
    def _beats(self, move1, move2):
        """Returns True if move1 beats move2."""
        if move1 == move2:
            return False
        if move1 == 'k' and move2 == 's':
            return True
        if move1 == 'p' and move2 == 'k':
            return True
        if move1 == 's' and move2 == 'p':
            return True
        return False
    
    def _counter(self, move):
        """Returns the move that beats the given move."""
        if move == 'k':
            return 'p'
        elif move == 'p':
            return 's'
        elif move == 's':
            return 'k'
        return 'k'
    
    def _find_sequence_pattern(self, sequence):
        """
        Finds repeating patterns in move sequences and predicts the next move.
        Returns the predicted move based on pattern matching.
        """
        if len(sequence) < 2:
            return None
        
        # Look for repeating subsequences
        for pattern_len in range(min(5, len(sequence) // 2), 0, -1):
            pattern = sequence[-pattern_len:]
            
            # Count how many times this pattern appears
            matches = 0
            for i in range(len(sequence) - pattern_len):
                if sequence[i:i + pattern_len] == pattern:
                    matches += 1
            
            # If pattern repeats at least twice, predict based on what follows
            if matches >= 2:
                # Find what typically follows this pattern
                for i in range(len(sequence) - pattern_len - 1):
                    if sequence[i:i + pattern_len] == pattern:
                        next_move = sequence[i + pattern_len]
                        return next_move
        
        return None
    
    def _frequency_analysis(self):
        """
        Analyzes frequency of opponent's moves and returns counter to most frequent.
        """
        if not self._history:
            return None
        
        k_count = self._history.count('k')
        p_count = self._history.count('p')
        s_count = self._history.count('s')
        
        # Get the most frequent move
        max_count = max(k_count, p_count, s_count)
        if max_count == 0:
            return None
        
        if k_count == max_count:
            most_frequent = 'k'
        elif p_count == max_count:
            most_frequent = 'p'
        else:
            most_frequent = 's'
        
        return self._counter(most_frequent)
    
    def _predict_opponent_move(self):
        """
        Attempts to predict opponent's next move using various strategies.
        Returns (predicted_move, strategy_name, confidence)
        """
        if len(self._history) == 0:
            return None, 'random', 0.0
        
        # Strategy 1: Pattern matching
        pattern_prediction = self._find_sequence_pattern(self._history)
        if pattern_prediction:
            return self._counter(pattern_prediction), 'pattern_match', 0.6
        
        # Strategy 2: Frequency analysis
        frequency_prediction = self._frequency_analysis()
        if frequency_prediction:
            return frequency_prediction, 'frequency', 0.5
        
        # Strategy 3: Exploit recent moves (last 3 moves)
        if len(self._history) >= 3:
            recent = self._history[-3:]
            recent_counts = {
                'k': recent.count('k'),
                'p': recent.count('p'),
                's': recent.count('s')
            }
            most_recent = max(recent_counts, key=recent_counts.get)
            return self._counter(most_recent), 'recent_bias', 0.4
        
        return None, 'random', 0.0
    
    def _metastrategy(self):
        """
        Apply metastrategies to counter the opponent's counter-strategies.
        Detects if opponent is adapting to our pattern and changes approach.
        """
        if len(self._history) < 4 or len(self._ai_history) < 4:
            return None
        
        # Check if opponent is countering our moves
        opponent_counters = 0
        for i in range(len(self._ai_history) - 4, len(self._ai_history)):
            if self._beats(self._history[i], self._ai_history[i]):
                opponent_counters += 1
        
        # If opponent is successfully countering us 75% of the time, switch strategy
        if opponent_counters >= 3:
            return 'switch_strategy'
        
        return None
    
    def anna_siirto(self):
        """
        Generate next move using the elite AI strategy.
        """
        # Apply metastrategy if needed
        meta = self._metastrategy()
        if meta == 'switch_strategy':
            # Randomize to break predictability
            return random.choice(['k', 'p', 's'])
        
        # Get prediction
        prediction, strategy, confidence = self._predict_opponent_move()
        
        if prediction:
            return prediction
        
        # Fallback: random choice
        return random.choice(['k', 'p', 's'])
    
    def aseta_siirto(self, siirto):
        """
        Record opponent's move for learning.
        """
        self._history.append(siirto)
        
        # Keep history bounded
        if len(self._history) > self._history_size:
            self._history.pop(0)
    
    def aseta_oma_siirto(self, siirto):
        """
        Record our own move for metaanalysis.
        """
        self._ai_history.append(siirto)
        if len(self._ai_history) > self._history_size:
            self._ai_history.pop(0)
    
    def reset(self):
        """Reset learning history."""
        self._history = []
        self._ai_history = []
        self._strategy_scores = {
            'history_match': 0,
            'frequency': 0,
            'random': 0
        }
