# Frogger 🐸
A Classic remake of the arcade game Frogger built with Python and Pygame-CE

## Description 
Guide your frog safely across busy roads with cars and rivers with floating logs. Try to reach the finish line at the top to advance to the next level with increased difficulty. 

#### Features 
- Multiple randomly generated levels
- Car lanes with varying speeds and directions
- Water lanes with moving logs
- Score tracking and a high score system
- Sound effects and background music (all homemade)
- Multiple frog lives
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

Help your frog cross the road and rivers safely! You have 3 lives, so if you get hit or fall in the water you can restart until you run out of lives. use the controls above to restart or quit the game

## Technical Details

- **Resolution**: 1280×960
- Display is windowed (non-resizeable)
- 2D tile-based grid using square tiles
- Snappy grid aligned movement

## Project Structure

- **frogger/**
  - **assets/**
    - `*.png`          — game sprites and textures  
    - **sounds/**      
      - audio files (sound effects, music)
  - **scripts/**
    - `main.py`        — game loop
    - `constants.py`   — store fixed values
    - `level.py`       — level setup and progression  
    - `player.py`      — player logic  
    - `car.py`         — car logic and behavior
    - `car_lane.py`    — road lane behavior  
    - `water_lane.py`  — water lane behavior  
    - `log.py`         — log logic and behavior
    - `score.py`       — score tracking  
    - `highscore.py`   — highscore logic 
    - `highscores.json` — highscore storage
    - `gameover.py`    — game over screen and logic
  - `README.md`        — project documentation  
  - `requirements.txt` — Python dependencies
  - `.gitignore`       — Ignore unnecessary files

## Credits

- Inspired by classic Frogger arcade game (1981)
- All sprites, sounds and music created in-house
- Made for Capgemini Python Project

## License

- This project is for educational purposes
