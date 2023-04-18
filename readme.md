# Minesweeper Autosolver

## The Idea

Welcome to the minesweeper solver. This program written in Python solves minesweeper on its own. 

The program uses the open-cv library and pyautogui to find the minesweeper game on your computer screen and then clicks the mine fields automaticaly with your cursor.

## Installation

You just need to have Python and create a virtual environment. Install packages from "requirements.txt" into your venv and you're good to go.

## Usage

### Navigate to main.py. There you have 2 lines of code:

* test.performRandomSolving()
    
    - runs the program without logic. Program randomly clicks on undiscovered fields and automaticaly restarts the game. Stops when wins (never happens)
    
    ----

* gl.performOptimalSolving()

    - runs the program with logic. Its goal is to win the game. If it fails due to random factor of the game, restarts the game automatically. Stops when wins.



### In file test.py you have to flags for testing:

* TESTING = False

    - If True runs tests with terminal output.

    -----

* SHOW_IMAGE_PROCESSING = False

    - If True shows every step of image processing for every cycle for testing. If you want to use the program for solving this should definitely be False.
