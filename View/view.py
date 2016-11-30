#!/usr/bin/env python

"""view.py: Reversi Game User Interface Code.

This program provides several classes related to reversi game user interface.
It uses Tkinter module to provide the graphical view of the game and capture
the user button-press or key-press events. The program also communicates with
"model.py" module and updates the graphical view when the model file changes.

"""

__author__ = "Tiansong Cui"
__email__ = "tcui@usc.edu"

from Tkinter import *
import time
import sys
sys.path.append("..")
from Model.model import *


class Square:
    """View of the unit square in the board.

    8*8 squares are created at the beginning of the Reversi Game. Once the
    squares are created, they remain unchanged until the game ends.

    Attributes:
        canvas (Tkinter.Canvas): The canvas of the game view.
        id (Tkinter.Canvas object ID): The ID of the created square.

    """

    def __init__(self, canvas, color, x, y, scale):
        """Create a square according to the coordinates.

        Args:
            canvas (Tkinter.Canvas): The canvas of the game view.
            color (str): Color of the square.
            x (int): x coordinate.
            y (int): y coordinate.
            scale (int): Side length of the square unit.

        """
        
        self.canvas = canvas
        x_start = x * scale
        y_start = y * scale
        x_end = (x + 1) * scale
        y_end = (y + 1) * scale
        self.id = canvas.create_rectangle(x_start, y_start, x_end, y_end,
                                          fill=color)

                                          
class Piece:
    """View of the unit piece in the board.

    8*8 squares are initialized at the center of each square. Each piece keeps
    updating in response to the change of the game model.

    Attributes:
        canvas (Tkinter.Canvas): The canvas of the game view.
        id (Tkinter.Canvas object ID): The ID of the created piece.

    """
    
    def __init__(self, canvas, fill_color, x, y, scale, size):
        """Initialize a piece at the center of the corresponding square.

        Args:
            canvas (Tkinter.Canvas): The canvas of the game view.
            fill_color (str): Fill-color of the piece.
            x (int): x coordinate.
            y (int): y coordinate.
            scale (int): Side length of the square unit.
            size (int): Diameter of the piece unit in the game.

        """

        self.canvas = canvas
        x_start = x * scale + (scale - size) // 2 
        y_start = y * scale + (scale - size) // 2 
        x_end = x_start + size
        y_end = y_start + size 
        self.id = canvas.create_oval(x_start, y_start, x_end, y_end,
                                     fill=fill_color)


    def config(self, fill_color, outline_color):
        """Updates the fill-color and outline-color.

        Piece color representation table:
        | which side to play |     condition     | fill-color | outline-color |
        |    black/write     | occupied by black |   black    |     black     |
        |    black/write     | occupied by write |   write    |     write     |
        |       black        |   movable piece   |   gray30   |     black     |
        |       write        |   movable piece   |   gray70   |     black     |
        |       black        | possible to place |   green    |     black     |
        |       write        | possible to place |   green    |     write     |
        |    black/write     |       empty       |   green    |     green     |
        

        Args:
            fill_color (str): Fill-color of the piece.
            outline_color (str): Outline-color of the piece.

        """

        self.canvas.itemconfig(self.id, fill=fill_color, outline=outline_color)


class Game_View:
    """User interface of the reversi game.

    This class provides the graphical view of the game and capture the user
    key-press events. The class also communicates with "model.py" module and
    updates the graphical view when the model file changes.

    Attributes:
        tk (Tkinter.Tk): The top level module of the game view.
        canvas (Tkinter.Canvas): The canvas of the game view.
        game_model (Game_Model): The corresponding game model.
        square_list (2D array): 8*8 squares showing the game board.
        piece_list (2D array): 8*8 pieces on the board.

    """

    def __init__(self, game_model, scale, size):
        """Initialize the game view.

        Args:
            game_model (Game_Model): Model of the reversi game.
            scale (int): Side length of the square unit.
            size (int): Diameter of the piece unit in the game.

        """
        
        # Initialize the tk, show the game name
        self.tk = Tk()
        self.tk.title("Reversi Game")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        
        # Initialize the canvas, set the size of the canvas 
        self.canvas = Canvas(self.tk, width=8*scale, height=8*scale, bd=0,
                             highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        
        # Initialize the game_model of the game_view
        self.game_model = game_model
        
        # Set the key-press functions
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)
        self.canvas.bind_all("<KeyPress-Up>", self.move_up)
        self.canvas.bind_all("<KeyPress-Down>", self.move_down)
        self.canvas.bind_all("<space>", self.place)
        self.canvas.bind_all("<Escape>", self.escape)
        
        # Initialize the board using 8*8 squares
        self.square_list = [[Square(self.canvas, "green", i, j, scale)
                             for j in range(8)] for i in range(8)]
        
        # Initialize the 8*8 pieces on the board
        self.piece_list = [[Piece(self.canvas, "green", i, j, scale, size)
                            for j in range(8)] for i in range(8)]
        
        self.tk.update_idletasks()
        self.tk.update()

        
    def update(self, side, location, current_table, available_table):
        """Updates the game view given the game model.

        Piece condition representation table:
        | which side to play |    condition     |current_table|available_table|
        |    black/write     |occupied by black |      1      |     False     |
        |    black/write     |occupied by write |     -1      |     False     |
        |    black/write     |possible to place |      0      |     True      |
        |    black/write     |      empty       |      0      |     False     |
        
        The x and y coordinates of the movable piece is given by location[0]
        and location[1].

        Args:
            side (int): 1 if it is the black side to play, -1 if it is the
                        write side to play.
            location (array): x and y coordinates of the movable piece.
            current_table (2D array): Identify pieces that are occupied.
            available_table (2D array): Identify locations that are possible to
                                        place the piece.

        """

        for i in range(8):
            for j in range(8):
                piece = self.piece_list[i][j]
                
                if current_table[i][j] == 0:
                    piece.config("green", "green")
                elif current_table[i][j] == 1:
                    piece.config("black", "black")
                elif current_table[i][j] == -1:
                    piece.config("white", "white")

                if available_table[i][j] == True:
                    if side == 1:
                        piece.config("green", "black")
                    else:
                        piece.config("green", "white")
        
        piece = self.piece_list[location[0]][location[1]]
        if side == 1:
            piece.config("gray30", "black")
        else:
            piece.config("gray70", "black")
        
        self.tk.update_idletasks()
        self.tk.update()
    
    
    def move_left(self, evt):
        # Move left when the player presses the <left> arrow
        self.game_model.move("left")
        
        
    def move_right(self, evt):
        # Move right when the player presses the <right> arrow
        self.game_model.move("right")


    def move_up(self, evt):
        # Move up when the player presses the <up> arrow
        self.game_model.move("up")


    def move_down(self, evt):
        # Move down when the player presses the <down> arrow
        self.game_model.move("down")


    def place(self, evt):
        # Place the piece when the player presses the <Space> button
        self.game_model.place()
    
    
    def escape(self, evt):
        # Exit the game when the player presses the <Esc> button
        self.game_model.escape()


class Pre_Game_View:
    """User interface of the pre-game selection window.

    This class provides the graphical view of the pre-game selection window.
    It captures the player's selection of the reversi game variables. When the
    player presses the "play" button, this window is closed and the reversi
    game starts with the variables selected by the player.

    Attributes:
        tk (Tkinter.Tk): The top level module of the pre-game selection window.
        pre_game_model (Pre_Game_Model): The corresponding pre-game model.
        file_name (StringVar): File that indicates the initial condition.
        music (BooleanVar): Whether to play music during the game.
        mode (IntVar): 1 if the player chooses to play with an easy AI;
                       2 if the player chooses to play with a hard AI;
                       0 if the player chooses to play with another player.
        AI_side (IntVar): 1 if AI plays black; -1 if AI plays write.                     

    """
    
    def __init__(self, pre_game_model):
        # Initialize the tk
        self.tk = Tk()
        self.pre_game_model = pre_game_model
        
        # Set the title 
        self.tk.title("Make a selection")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        
        # Add all the buttons
        self.add_introduction()
        self.add_restore_selection()
        self.add_music_selection()
        self.add_mode_selection()
        self.add_AI_side_selection()
        self.add_start_button()
    
    
    def add_introduction(self):
        # Add the pre-game instruction
        text = Text(self.tk, width=50, height=5)
        text.insert(INSERT, "Welcome to Reversi Game!\n")
        text.insert(END, "Please make a selection and start the game.\n")
        text.pack()
    
    
    def add_restore_selection(self):
        """A radiobutton selects the initial condition file name.
        
        If the player chooses to start a new game, the file_name is
        set as "Model/default.log"; If the player chooses to restore from the
        previous game, it is set as "Model/default.log".
        
        """
        
        self.file_name = StringVar()
        self.file_name.set("Model/default.log")
        
        button1 = Radiobutton(self.tk, text="Start a New Game",
                              variable=self.file_name, value="Model/default.log",
                              height=2, width = 30)
        button2 = Radiobutton(self.tk, text="Restore from Previous Game",
                              variable=self.file_name, value="Model/current.log",
                              height=2, width = 30)
        
        button1.pack()
        button2.pack()
    
    
    def add_music_selection(self):
        """ A checkbutton that selects whether to play music during the game.
        
        The music variable is set as True if the player chooses to listen to
        music while playing the game; otherwise it is set as False.
        
        """
        
        self.music = BooleanVar()
        
        button = Checkbutton(self.tk, text = "Music", variable = self.music,
                             onvalue = True, offvalue = False, height=3,
                             width = 30)
        
        button.pack()
        button.select()
        
    
    def add_mode_selection(self):
        """A radiobutton that selects the mode of the game.
        
        The mode variable is set as 1 if the player chooses to play with an
        easy AI, 2 if the player chooses to play with a hard AI, and 0 if the
        player chooses to play with another player.
        
        """
        
        self.mode = IntVar()
        self.mode.set(1)
        
        button1 = Radiobutton(self.tk, text="One Player Game - Easy",
                              variable=self.mode, value=1,
                              height=2, width = 30)
        button2 = Radiobutton(self.tk, text="One Player Game - Hard",
                              variable=self.mode, value=2,
                              height=2, width = 30)
        button3 = Radiobutton(self.tk, text="Two Player Game",
                              variable=self.mode, value=0,
                              height=2, width = 30)
        
        button1.pack()
        button2.pack()
        button3.pack()
    
    
    def add_AI_side_selection(self):
        """ A checkbutton that selects the AI side.
        
        The AI_side variable is set as 1 if AI plays black, and -1 if AI
        plays write.
        
        """

        self.AI_side = IntVar()
        self.AI_side.set(-1)
        
        button = Checkbutton(self.tk, text = "AI plays black",
                             variable = self.AI_side, onvalue = 1,
                             offvalue = -1, height=3, width = 30)
        
        button.pack()
    
    
    def start_game(self):
        # Call the model function to start the game
        self.pre_game_model.start_game()
    
    
    def add_start_button(self):
        # When player presses the "Play" button, the game starts
        button = Button(self.tk, text="Play", command=self.start_game,
                        height=2, width = 10)
                        
        button.pack()