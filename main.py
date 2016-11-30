#!/usr/bin/env python

"""main.py: Reversi Game Main Function.

This is the main program of the reversi game. It starts with the pre-game
model. After the user makes a section, it initializes a game for the user to
play. When the game ends or the user presses the "ESC" button, the program
exits.

Example:
    $ python main.py
        
"""

__author__ = "Tiansong Cui"
__email__ = "tcui@usc.edu"

from Model.model import *
import sys
import time

SCALE = 65  # side length of the square unit in the game
SIZE = 55  # diameter of the piece unit in the game

# start the pre_game model
pre_game = Pre_Game_Model()

# wait until the user to make a selection
while pre_game.selection_complete == False:
    pre_game.pre_game_view.tk.update_idletasks()
    pre_game.pre_game_view.tk.update()
    time.sleep(0.01)

# end the pre_game model
pre_game.pre_game_view.tk.destroy()

# start the game model based on user's selection
new_game = Game_Model(SCALE, SIZE, pre_game.mode, pre_game.AI_side,
                      pre_game.music, pre_game.file_name)

# wait until the game ends or the user presses the "ESC" button
while new_game.escape_flag == False:
    new_game.game_view.tk.update_idletasks()
    new_game.game_view.tk.update()
    time.sleep(0.01)

# program exits
sys.exit()


if __name__ == "__main__":
    app.run()