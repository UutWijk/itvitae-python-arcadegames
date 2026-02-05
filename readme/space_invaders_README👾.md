# Space Invaders 👾
A Classic remake of the arcade game Space Invaders built with Python and Pygame-CE

## Description 
Shoot to destroy the invading aliens before they reach your ship. Reach a new high score by clearing increasingly aggressive waves of space invaders.

#### Features 
- Multiple levels, invaders shoot more often every level.
- Invaders move faster as more of them are destroyed.
- 3 Lives.
- Score tracking and a high score system.
- Original sound effects.
- Destructible environment.
- Unique handmade sprites

- Car speed increases with each level completed, and random generation ensures unique layouts every level

## Controls 

| Key (on arcade) | Key (on computer) | Action |
|----|-----|--------|
| `↑` | `w` | Move Up 
| `↓` | `s` | Move Down |
| `←` | `a` |  Move Left |
| `→` | `d` | Move Right |
| `A` | `Spacebar` | Restart (when game over) |
| `B` | `Escape` | Back to Main menu

##  Installation

#### Requirements:
- Python 3.12 or 3.14 (*Compatible with 3.12.3 and 3.14.2*)
- Pygame-CE 2.5.6 

#### Steps to install
1. Clone or download this repository from GitHub
2. Install dependencies:

   ```
   python -m pip install -r requirements.txt
   ```

#### How to Run

1. **With the Launcher**  
   Simply open the launcher and click "Start Game."

2. **Manually (without the launcher)**  
   You can run the game directly for development or testing:

   - From the root directory:
     ```bash
     python scripts/main.py   # Windows
     python3 scripts/main.py  # Linux/macOS
     ```

   - From the `scripts` folder:
     ```bash
     python main.py           # Windows
     python3 main.py          # Linux/macOS
     ```
## How to Play

Shoot the space invaders before they reach your ship! The game is over when the invaders reach the bottom, or when you run out of lives when getting hit by invaders' shooting.

## Technical Details

- **Resolution**: 1280×960
- Display is windowed (non-resizeable)

## Project Structure

- **Space_Invaders/**
  - **assets/**
    - `*.png`          — game sprites and textures  
    - **audio/**      
      - audio files (sound effects, music)
    - **fonts/**
      - typeface used
  - **scripts/**
    - `assets.py`        — initialising the textures and sound
    - `Bullet.py`   — bullet logic for player and enemies
    - `Bunker.py`       — Bunker logic  
    - `constants.py`      — game constants
    - `enemy.py`         — enemy logic
    - `game.py`    — main game loop
    - `GameObject.py`  — abstract game object class 
    - `Player.py`         — player logic
    - `ufo.py`       — UFO object logic 
    - `UI.py`   — menu screens 
    - `High-Score.txt` — highscore storage
  - `README.md`        — project documentation  
  - `requirements.txt` — Python dependencies
  - `.gitignore`       — Ignore unnecessary files

## Credits

- Inspired by classic Space Invaders arcade game (1978)
- All sprites created in-house
- Made for Capgemini Python Project
- Made by Jochem, Bram and Zoey

## License

- This project is for educational purposes
