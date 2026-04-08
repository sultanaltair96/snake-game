# PySnake TUI - Specification Update

## Overview
Replaced pygame graphical implementation with a curses-based TUI version for terminal play. Both implementations coexist; the entry point auto-detects the best mode.

## Technical Changes

### New Module: `tui.py`
- Full TUI game implementation using Python stdlib `curses`
- Grid: 30 columns x 20 rows
- ASCII/Unicode visuals:
  - Snake: `#` (hash)
  - Food: `@` (at symbol)
  - Walls: `#` (hash)
  - Border corners: `+`

### Modified: `main.py`
- Auto-detects terminal capabilities
- Falls back to pygame if curses unavailable
- `--pygame` flag forces GUI mode
- Supports headless/remote environments

## Features (TUI)

| Feature | Implementation |
|---------|----------------|
| Grid | 30x20 cells |
| Movement | Arrow keys |
| Speed levels | easy (0.2s), medium (0.15s), hard (0.1s) |
| Score | +10 per food |
| Collision | Wall/self detection |
| Sound | `curses.beep()` |
| Visual effect | Screen flash on collision |
| Pause | `P` key |
| Exit to menu | `ESC` key |

## Game States
1. **NAME_INPUT** - Player enters name
2. **MAIN_MENU** - Play, Leaderboard, Quit
3. **PLAYING** - Active gameplay
4. **PAUSED** - Game paused
5. **GAME_OVER** - Score display + leaderboard

## High Score Persistence
- File: `highscores.json` (unchanged)
- Format: `{"name", "score", "date"}`
- Limit: Top 10 entries

## Running the Game

```bash
# Default (auto-detect TUI vs GUI)
python main.py

# Force pygame GUI
python main.py --pygame

# TUI requirements
# - Unix-like terminal (Linux, macOS, WSL)
# - TERM environment variable set
```

## Controls

| Key | Action |
|-----|--------|
| Arrow keys | Move snake |
| Enter | Confirm/Select |
| P | Pause/Resume |
| ESC | Return to menu |
| UP/DOWN | Menu navigation |
| LEFT/RIGHT | Change difficulty |

## Differences from Pygame Version
- No graphical rendering (terminal only)
- Screen flash instead of shake effect
- System beep instead of generated sounds
- Speed in seconds per tick vs FPS
- Simplified visuals (ASCII vs graphics)
