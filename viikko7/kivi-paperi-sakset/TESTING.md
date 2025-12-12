# Running Tests

## Quick Start

### Windows
```bash
run_tests.bat
```

### Linux/Mac
```bash
bash run_tests.sh
```

## Manual Test Execution

From the project root:
```bash
python -m pytest src/test_app.py -v
```

From the src directory:
```bash
cd src
python -m pytest test_app.py -v
```

## Test Coverage

The test suite includes 35+ tests covering:

### WebGameState Class Tests
- Initialization for all game modes (simple AI, advanced AI, elite AI, PvP)
- Move validation
- Move translation (k→Kivi, p→Paperi, s→Sakset)
- Round outcomes (draw, player 1 wins, player 2 wins)

### Flask API Tests
- Index page rendering
- Game start for all modes (including elite AI)
- Playing rounds with AI
- Playing rounds with elite AI
- PvP two-player flow
- Error handling (invalid game ID, invalid moves)
- Game state retrieval
- Multiple rounds handling

### Elite AI Tests
- Elite AI initialization
- Move counter logic (correct counters for all moves)
- Beat detection logic
- Opponent move recording and history management
- History size bounding
- Valid move generation
- Frequency analysis strategy
- Pattern detection in opponent sequences
- Pattern-based predictions
- Adaptive learning behavior
- API integration with elite AI

## Requirements

Tests require pytest, which is automatically installed when you run:
```bash
pip install pytest
```

Or if using the virtual environment:
```bash
.venv/Scripts/pip install pytest
```
