#!/usr/bin/env python

"""view.py: Reversi Game Model Code.

This program provides the reversi game model as well as the pre-game model.
It communites with "view.py" module and updates the graphical view when the
model file changes. The control functions are included in the "control.py"
module and the "AI.py" module provides the AI control algorithms.

"""

__author__ = "Tiansong Cui"
__email__ = "tcui@usc.edu"

import sys
sys.path.append("..")
from View.view import *
from Control.control import *
from Control.AI import *
import time
import pygame


class Game_Model:
    """Core model of the reversi game.

    This class provides the core model of the reversi game. It communiates with
    the view side (to update user interface view) and the control side (to get
    the corresponding result of an action.

    Attributes:
        game_model (Game_View): The corresponding game view.
        current_table (2D array): 8*8 values indicating the current condition
                                  of the board.
        available_table (2D array): 8*8 values indicating all the possible
                                    locations to place the piece.
        side (int): 1 if it is the black side to play, -1 if it is the
                    write side to play.
        location (array): x and y coordinates of the movable piece.
        current_table (2D array): Identify pieces that are occupied.
        available_table (2D array): Identify locations that are possible to
                                    place the piece.
        count (int): The number of pieces that are placed on the board.
        escape_flag (bool): Whether to end game or not.
        music (bool): Whether to play music during the game.
        mode (int): 1 if the player chooses to play with an easy AI;
                    2 if the player chooses to play with a hard AI;
                    0 if the player chooses to play with another player.
        AI_side (int): 1 if AI plays black; -1 if AI plays write.
        file_name (str): File that indicates the initial condition.

    """

    def __init__(self, scale, size, mode, AI_side, music, file_name):
        """Initialize the game model.

        Args:
            scale (int): Side length of the square unit.
            size (int): Diameter of the piece unit in the game.
            mode (int): 1 if the player chooses to play with an easy AI;
                        2 if the player chooses to play with a hard AI;
                        0 if the player chooses to play with another player.
            AI_side (int): 1 if AI plays black; -1 if AI plays write.
            music (bool): Whether to play music during the game.
            file_name (str): File that indicates the initial condition.

        """
    
        # initialize the game model
        self.current_table = [[0 for j in range(8)] for i in range(8)]
        self.game_view = Game_View(self, scale, size)
        self.location = [0,0]
        self.available_table = [[False for j in range(8)] for i in range(8)]
        self.side = 1
        self.count = 0
        self.escape_flag = False
        self.music = music
        self.mode = mode
        self.AI_side = AI_side
        
        # play music if needed
        if self.mode <= 1:
            pygame.mixer.music.load("Music/easy.mp3")
        else:
            pygame.mixer.music.load("Music/hard.mp3")
        
        if self.music == True:
            pygame.mixer.music.play(-1)
        
        # load the game starting condition
        self.load(file_name)


    def update_view(self):
        """Update the game view.
        
        When there is a change in the model, the game view will be updated
        correspondingly.

        """

        self.game_view.update(self.side, self.location, self.current_table, 
                              self.available_table)

       
    def move(self, direction):
        """Move the piece based on the given direction.
        
        When the player presses <up>, <down>, <left> or <right> on the,
        keyboard, the piece should make the corresponding movement.
        
        Args:
            direction (str): "left", "right", "up" or "down".

        """

        Move_Piece(self.current_table, self.location, direction)
        self.update_view()
    
    
    def place(self):
        """Place the piece at the current location.
        
        Will call the Place_Piece function. If the current location is not
        valid, then do nothing. Otherwise when a piece is placed, check whether
        we should switch side or not.

        """
    
        # check whether it is the last piece to place 
        if self.count == 63:
            update_flag = False
        else:
            update_flag = True
        
        # the Place_Piece function will return False if current location is
        # not valid
        if Place_Piece(self.current_table, self.location, self.side,
                       update_flag):
                       
            self.count += 1
            
            # by default we should switch side
            self.side = -self.side
            flag = Get_Available_Table(self.current_table, self.side,
                                       self.available_table)
                                       
            # if no valid place for the other side, switch back
            if flag == False:
                self.side = -self.side
                flag = Get_Available_Table(self.current_table, self.side,
                                           self.available_table)
                
                # if no valid place for both sides, end the game
                if flag == False:
                    self.end()
                    return

            
        self.update_view()
        
        # check whether the board is full
        if self.count == 64:
            self.end()
            return
        
        # check whether AI should place
        if self.mode > 0 and self.AI_side == self.side:
            self.AI_place()
        
    
    def AI_place(self):
        """Call AI to place the piece.

        This function will call Greedy (easy mode) or Min_MAX (hard mode)
        function to calculate the location that the AI will place. Then
        call self.place() function to place the piece.
        
        Note: In order to let the player realize the AI's decision, we manually
        delay an amount of time before AI place the piece.

        """
    
        if self.mode == 1:
            self.location = Greedy(self.current_table, self.side)[0]
            time.sleep(0.6)
        else:
            self.location = Min_Max(self.current_table, self.side, 3)[0]
            time.sleep(0.2)
        
        # flash and show the AI's decision
        for _ in range(6):
            self.side = -self.side
            self.update_view()
            time.sleep(0.1)
            
        self.place()
    
    
    def load(self, file_name):
        """Load the initial condition.

        When the game start, create the initial condition and calculate the
        available_table based on the initial condition. At the same time the
        side-switch and end-of-game conditions are also checked. 
        
        Args:
            file_name (str): "Model/default.log" or "Model/current.log".

        """

        file = open(file_name, "r").readlines()
        color = file[0].strip()
        if color == "W":
            self.side = -1
        else:
            self.side = 1
            
        self.count = Get_Current_Table(self.current_table, file[1:])
        if self.count == 64:
            self.end()
            return
            
        self.move("right")
        
        flag = Get_Available_Table(self.current_table, self.side,
                                   self.available_table)
                                   
        # check the side-switch and end-of-game conditions 
        if flag == False:
            self.side = -self.side
            flag = Get_Available_Table(self.current_table, self.side,
                                       self.available_table)
            if flag == False:
                self.end()
                return
        
        if self.mode > 0 and self.side == self.AI_side:
            self.AI_place()
            
        self.update_view()
    
    
    def escape(self):
        """Exit in the middle of the game and save the current condition.

        When the player presses <Esc>, save the current game condition to
        the file "Model/current.log" and exit the game.

        """
    
        current_file = open("Model/current.log", "w")
        
        Write_To_File(self.current_table, self.side, current_file)
        
        self.escape_flag = True
        
        return
    
    
    def end(self):
        """Exit the game when the end-of-game conditions are met.

        When the end-of-game conditions are met, exit the game and save the
        final result to the file "Model/result.log".

        """
    
        time.sleep(0.3)
        result_file = open("Model/result.log", "w")
        
        Write_To_File(self.current_table, self.side, result_file, True)
        
        self.escape_flag = True
        
        return


class Pre_Game_Model:
    """Model of the pre-game selection window.

    This class provides the model of the pre-game selection window.
    It captures the player's selection of the reversi game variables. When the
    player presses the "play" button, this window is closed and the reversi
    game starts with the variables selected by the player.

    Attributes:
        pre_game_model_view (Pre_Game_View): The corresponding pre-game view.
        file_name (str): File that indicates the initial condition.
        music (bool): Whether to play music during the game.
        mode (int): 1 if the player chooses to play with an easy AI;
                    2 if the player chooses to play with a hard AI;
                    0 if the player chooses to play with another player.
        AI_side (int): 1 if AI plays black; -1 if AI plays write. 
        selection_complete (bool): Whether the selection has been completed.

    """
    def __init__(self):
        # Initialize the game model and play the introduction music.
        
        self.pre_game_view = Pre_Game_View(self)
        self.mode = 0
        self.AI_side = -1
        self.music = True
        self.file_name = "default.log"
        self.selection_complete = False
        
        pygame.mixer.init()
        pygame.mixer.music.load("Music/start.mp3")
        pygame.mixer.music.play(-1)
    
    def start_game(self):
        # Get the corresponding variables and start the game.
    
        self.mode = self.pre_game_view.mode.get()
        self.AI_side = self.pre_game_view.AI_side.get()
        self.music = self.pre_game_view.music.get()
        self.file_name = self.pre_game_view.file_name.get()
        self.selection_complete = True
        pygame.mixer.music.stop()
        
        