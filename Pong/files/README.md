# Python Pong (pygame-ce)
A classic implementation of Pong (1972) built with Python 3.14 and pygame-ce. This project features smooth gameplay, collision physics and multiplayer

## Features
- Smooth Graphics: Optimized using the pygame-ce (Community Edition) framework.
- Dynamic Physics: Ball speed increases after every paddle hit.
- Modern Python: Leverages the latest performance improvements in Python 3.14.
- AI Opponent: Able to play against two AI opponents of varying difficulty. 

## Requirements
- Python 3.14 and above installed
- pygame-ce module installed
- pip (Python package manager)

## How to Play
- Left Joystick     movement Blue player (E for up and D for down on PC)
- Right Joystick    movement Orange player (only in multiplayer) (UP for up and DOWN for down on PC)
- A:                start multiplayer game (when in start screen)
- B:                select singleplayer mode:
                    - A: start "easy" game against AI
                    - B: start "hard" game against AI

## Project Structure
- main.py:          entry point of the game
- game.py           class definition and methods for the game loop
- ball.py:          class definition and methods for Ball objects
- paddle.py:        class definition and methods for Paddle objects
- ai_paddle.py:     class definition and methods for AI paddle object
- scoreboard.py:    class definition and methods for Scoreboard object
- sound.py:         class definition and methods for game sounds
- constants.py      class definition for game constants (framerate, screen size, paddle speed)
