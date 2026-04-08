# Python Snake Game - Specification

## Project Overview
- **Name**: PySnake
- **Type**: Classic arcade game recreation
- **Core Functionality**: Snake game using pygame with high score persistence and leaderboard
- **Target Users**: Casual gamers

## Technical Stack
- Python 3.8+
- pygame 2.x

## Features & Requirements

### 1. Game Mechanics
- Grid-based movement (20x20 cells, 30px each = 600x600 window)
- Snake grows by 1 segment when eating food
- Game over on wall collision or self-collision
- 3 speed levels (easy: 8fps, medium: 12fps, hard: 15fps)
- Score: +10 per food eaten

### 2. Player Registration
- Name input screen at game start (max 15 chars, alphanumeric)
- Validation: non-empty, no duplicates in session

### 3. High Score System
- **Storage**: `highscores.json`
- **Fields per entry**: name, score, date (YYYY-MM-DD)
- **Limit**: Top 10 scores
- **Format**: Sorted descending by score

### 4. Leaderboard
- Displayed on game over screen
- Shows rank, name, score, date
- Top 10 entries only

### 5. Visual Design
| Element | Color |
|---------|-------|
| Background | Dark (#1a1a2e) |
| Grid lines | Subtle (#16213e) |
| Snake head | Lime (#00ff88) |
| Snake body | Gradient green (#00ff88 -> #00aa55) |
| Food | Red (#ff4757) with pulse animation |
| UI text | White (#ffffff) |
| Score display | Cyan (#00d4ff) |

- **Screen shake**: 10px amplitude, 300ms duration on collision
- Snake uses rounded rectangles

### 6. Sound Effects
| Event | Sound Type |
|-------|------------|
| Eat food | Short blip (440Hz, 100ms) |
| Game over | Low buzz (200Hz, 500ms) |
| Menu navigation | Click (800Hz, 50ms) |

- Sound generated programmatically using pygame mixer (no external files needed)

### 7. Game States
1. **NAME_INPUT** - Player enters name
2. **MAIN_MENU** - Play, Leaderboard, Quit options
3. **PLAYING** - Active gameplay
4. **GAME_OVER** - Show score, leaderboard, retry/menu options

## File Structure
```
snake-game/
├── SPEC.md
├── main.py          # Entry point
├── game/
│   ├── __init__.py
│   ├── constants.py # Colors, sizes, paths
│   ├── state.py     # GameState enum, StateManager
│   ├── snake.py     # Snake class
│   ├── food.py      # Food class
│   ├── score.py     # ScoreManager (JSON)
│   ├── sounds.py    # SoundManager
│   ├── screen.py    # Screen effects (shake)
│   └── ui.py        # UI components
└── highscores.json  # Generated on first run
```

## Acceptance Criteria
- [ ] Game launches without errors
- [ ] Name input accepts valid names, rejects empty/invalid
- [ ] Snake moves smoothly, responds to arrow keys
- [ ] Food spawns randomly, snake grows on eating
- [ ] Collision with wall/self triggers game over + screen shake
- [ ] Sound effects play for eat/game over events
- [ ] High scores persist across sessions (JSON)
- [ ] Leaderboard shows top 10 with name/score/date
- [ ] All three speed modes work correctly

## Controls
| Key | Action |
|-----|--------|
| Arrow keys | Move snake |
| Enter | Confirm/Select |
| Escape | Back to menu |
| P | Pause (during play) |
