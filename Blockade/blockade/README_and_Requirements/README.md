# BLOCKADE
An arcade game from the 70's recreated in pygame-ce.

The goal is to live as long as possible, while trying to block off the other player. Creating a 'blockade'.

You win the round when the other player hits the wall. You win the game after winning 3 rounds. A draw happens when both player's collide, draws do not give points.

## Features:
* Simple arcade-style graphics.
* Recreation of retro gameplay.

## Requriements:
See requirements.txt

## How To Play:
* When the game starts, press any button to begin.
* As soon as a button is pressed, the players will start moving on their own.
* You will play untill someone has 3 wins, (draws are possible).
* When a player has 3 wins, a prompt will appear on screen asking if you want to try again: use the 'A' button to reset the game.
* If you want to return to the main menu/game selection menu, press the 'B' button.

### Player 1 controls: 
* Player 1 uses E, S, D, F to change direction: 
* E = UP
* S = LEFT 
* D = DOWN
* F = RIGHT

### Player 2 controls: 
* Player 2 uses the arrow keys to change direction:
* UP = UP 
* LEFT = LEFT
* DOWN = DOWN
* RIGHT = RIGHT

## Project Structure:
* We have an executable. When launching it, you will see a menu where you can choose what game you want to play.
* Main.py is our launcher that handels the main menu
* Each game has their seperate .py file that the launcher calls to play the game
* For blockade: Player.py makes the player class that gets used in the game.
* For blockade: Sound.py handles the soundeffects, the assets for this are stored in the asset folder.
