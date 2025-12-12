# Kivi-Paperi-Sakset (Rock-Paper-Scissors)

A web-based rock-paper-scissors game built with Flask, featuring multiple game modes including AI opponents with different difficulty levels and player-vs-player mode.

## Features

- 🎮 **Three Game Modes:**
  - **Simple AI**: Basic computer opponent with predictable patterns
  - **Advanced AI**: Intelligent opponent that learns from your moves
  - **Player vs Player**: Two-player mode with turn-based gameplay

- 🎨 **Modern Web Interface:**
  - Responsive design that works on desktop and mobile
  - Real-time score tracking
  - Visual feedback for game results
  - Clean, intuitive UI with gradient design

- 🧪 **Comprehensive Test Suite:**
  - 23 automated tests covering all functionality
  - Tests for game logic, API endpoints, game flows, and game ending conditions
  - Easy to run with provided scripts
  - Tests automatically adapt to configured rounds-to-win setting

## Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

### Setup

1. Clone or navigate to the repository:
```bash
cd kivi-paperi-sakset
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install flask pytest
```

## Running the Application

### Start the Web Server

From the project root:
```bash
cd src
python app.py
```

The application will start on **http://localhost:5000**

Open your web browser and navigate to `http://localhost:5000` to play!

### Playing the Game

1. **Select a game mode** by clicking one of the three buttons:
   - Tekoäly (helppo) - Simple AI
   - Tekoäly (vaikea) - Advanced AI
   - Kaksinpeli - Two players

2. **Make your move** by clicking Kivi (Rock), Paperi (Paper), or Sakset (Scissors)

3. **View results** - The game displays:
   - Each player's move
   - Current scores
   - Who won the round

4. **Play multiple rounds** - Keep playing to build up scores

5. **Reset** - Click "Aloita uusi peli" to start fresh

## Running Tests

### Quick Test Execution

**Windows:**
```bash
run_tests.bat
```

**Linux/Mac:**
```bash
bash run_tests.sh
```

### Manual Test Execution

```bash
# From project root
python -m pytest src/test_app.py -v

# From src directory
cd src
python -m pytest test_app.py -v
```

All 23 tests should pass, covering:
- Game initialization
- Move validation
- Round outcomes
- Game ending conditions (winning required rounds)
- API endpoints
- PvP game flow
- Error handling
- Preventing play after game ends

## Project Structure

```
kivi-paperi-sakset/
├── src/
│   ├── app.py                    # Flask web application
│   ├── test_app.py              # Automated tests
│   ├── index.py                 # Terminal-based game launcher
│   ├── kivi_paperi_sakset.py    # Base game class
│   ├── kps_pelaaja_vs_pelaaja.py # PvP implementation
│   ├── kps_tekoaly.py           # Simple AI implementation
│   ├── kps_parempi_tekoaly.py   # Advanced AI implementation
│   ├── luo_peli.py              # Game factory
│   ├── tekoaly.py               # Simple AI logic
│   ├── tekoaly_parannettu.py    # Advanced AI logic
│   ├── tuomari.py               # Game referee/scorer
│   └── templates/
│       └── index.html           # Web interface
├── run_tests.bat                # Windows test runner
├── run_tests.sh                 # Linux/Mac test runner
├── pyproject.toml              # Project configuration
├── TESTING.md                  # Testing documentation
└── README.md                   # This file
```

## Technologies Used

- **Backend:** Flask 3.0+ (Python web framework)
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Testing:** pytest 7.0+
- **Architecture:** RESTful API with session-less game state management

## Configuration

### Changing Rounds to Win

The game ends when one player wins a configurable number of rounds (default: 3).

**To change this setting:**

Edit `src/app.py` and modify the `ROUNDS_TO_WIN` constant at the top of the file:

```python
# Game configuration - change this value to set rounds needed to win
ROUNDS_TO_WIN = 3  # Change to any number you want
```

This single change will automatically update:
- Backend game logic
- Frontend display
- All test cases

After changing the value, restart the Flask server for changes to take effect.

## Game Logic

### Move Rules
- **Rock (Kivi)** beats Scissors
- **Paper (Paperi)** beats Rock
- **Scissors (Sakset)** beats Paper

### Winning the Game
- First player to win `ROUNDS_TO_WIN` rounds wins the game (default: 3)
- Draw rounds don't count towards the win total
- Game buttons are disabled once a winner is declared

### AI Opponents

**Simple AI (`Tekoaly`):**
- Cycles through moves in a predictable pattern: Rock → Paper → Scissors
- Good for beginners

**Advanced AI (`TekoalyParannettu`):**
- Uses memory-based pattern recognition
- Learns from your previous moves
- Predicts your next move based on history
- More challenging opponent

### PvP Mode
- Turn-based gameplay
- Player 1 selects their move (hidden from Player 2)
- Player 2 then selects their move
- Both moves revealed simultaneously with results

## API Endpoints

### `POST /api/start_game`
Start a new game session.
```json
Request: {"game_type": "simple_ai" | "advanced_ai" | "pvp"}
Response: {"success": true, "game_id": "uuid", "player2_name": "..."}
```

### `POST /api/play_round`
Play a round in the game.
```json
Request: {"game_id": "uuid", "move": "k" | "p" | "s"}
Response: {"player1_move": "...", "player2_move": "...", "player1_score": 0, ...}
```

### `GET /api/get_state`
Get current game state.
```
Query: ?game_id=uuid
Response: {"player1_score": 0, "player2_score": 0, "draws": 0}
```

## Development

### Adding New Features

The codebase follows object-oriented design principles:
- `KiviPaperiSakset` is the abstract base class
- Each game mode extends this base class
- `Tuomari` handles scoring logic
- AI classes are independent and swappable

### Extending AI

To add a new AI opponent:
1. Create a new AI class in `src/`
2. Implement `anna_siirto()` and `aseta_siirto()` methods
3. Add game mode to `luo_peli.py`
4. Update `app.py` to support the new mode
5. Add corresponding tests

## License

MIT License

## Contributors

- Original terminal version: Matti Luukkainen
- Web interface: Created with GitHub Copilot

## Troubleshooting

**Flask not found:**
```bash
pip install flask
```

**Tests not running:**
```bash
pip install pytest
```

**Port 5000 already in use:**
Edit `src/app.py` and change the port number in the last line:
```python
app.run(debug=True, port=5001)  # Change to any available port
```

**Virtual environment not activating on Windows:**
```bash
# Use PowerShell
.venv\Scripts\Activate.ps1

# Or Git Bash
source .venv/Scripts/activate
```
