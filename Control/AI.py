#!/usr/bin/env python

"""AI.py: Reversi Game AI Control Code.

This program provides the AI control functions used in the reversi game when
the player selects "one-player" mode. Two difficulty levels are included in
this program.

The AI decision is based on a pre-defined weight matirx, which will direct the
AI to place at better positions (e.g., the 4 corners). In the easy difficulty
level, the AI will use a greedy algorithm, and in the hard level, the AI will
use a min-max algorithm.

"""

__author__ = "Tiansong Cui"
__email__ = "tcui@usc.edu"

from control import *

# weight matrix used in this program
WEIGHT_MATRIX = [[99, -8, 8, 6, 6, 8, -8, 99],
                 [-8, -24, -4, -3, -3, -4, -24, -8],
                 [8, -4, 7, 4, 4, 7, -4, 8],
                 [6, -3, 4, 0, 0, 4, -3, 6],
                 [6, -3, 4, 0, 0, 4, -3, 6],
                 [8, -4, 7, 4, 4, 7, -4, 8],
                 [-8, -24, -4, -3, -3, -4, -24, -8],
                 [99, -8, 8, 6, 6, 8, -8, 99]]


def Weight_Calculation(table, side):
    """Calculate the weight of a given table for one player side.

    Args:
        table (2D array): 8*8 values indicating the current condition
                          of the board.
        side (int): 1 if we calculate the weight of the black side,
                    -1 if it is thethe weight of the white side.
    
    Returns:
        weight (int): Calculated weight of the given table.

    """

    weight = 0
    
    for i in range(8):
        for j in range(8):
            weight += table[i][j] * side * WEIGHT_MATRIX[i][j]
        
    return weight


def Greedy(current_table, side):
    """Find the best location to place a piece based on greedy algorithm.
    
    This algorithm tries to place the piece at every possible location and
    select the location that leads to the maximum weight.

    Args:
        current_table (2D array): 8*8 values indicating the current condition
                                  of the board.
        side (int): 1 if we calculate the weight of the black side,
                    -1 if it is thethe weight of the white side.
    
    Returns:
        location (array): x and y axes of the calculated location.
        max_weight (int): Maximum weight that is achieved by placing at the
                          above location. It is used when called by Min_Max
                          function.

    """
    
    max_weight = -65535
    location = [-1, -1]
    
    for x in range(8):
        for y in range(8):
            temp_table = [[current_table[i][j] for j in range(8)]
                          for i in range(8)]
            
            # try to place the piece at a given location
            # calculate the weight from the result
            if Place_Piece(temp_table, [x,y], side):
                temp_weight = Weight_Calculation(temp_table, side)
                # keey the best location and maximum weight
                if temp_weight > max_weight:
                    max_weight = temp_weight
                    location[:] = [x,y]
    
    return (location, max_weight)


def Min_Max(current_table, side, depth):
    """Find the best location to place a piece based on min-max algorithm.

    This algorithm tries to place the piece at every possible location.
    Different from the greedy algorithm, this algorithm looks deeper and tries
    to maximize its rewards assuming the opponent also maximizes its rewards.
    
    Args:
        current_table (2D array): 8*8 values indicating the current condition
                                  of the board.
        side (int): 1 if we calculate the weight of the black side,
                    -1 if it is thethe weight of the white side.
        depth (int): Depth of the min-max algorithm.
    
    Returns:
        location (array): x and y axes of the calculated location.
        max_weight (int): Maximum weight that is achieved by placing at the
                          above location. It is used when called by Min_Max
                          function.

    """

    # when depth is 0, it is equavilent to greedy algorithm
    if depth == 0:
        return Greedy(current_table, side)

    max_weight = -65535
    location = [-1, -1]
    
    for x in range(8):
        for y in range(8):
            temp_table = [[current_table[i][j] for j in range(8)]
                          for i in range(8)]
            
            if Place_Piece(temp_table, [x,y], side):
                # calculate the opponent's optimal decision
                temp_weight = -Min_Max(temp_table, -side, depth-1)[1]
                if temp_weight >= max_weight:
                    max_weight = temp_weight
                    location[:] = [x, y]

    return (location, max_weight)