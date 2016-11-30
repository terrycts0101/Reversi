#!/usr/bin/env python

"""control.py: Reversi Game General Control Code.

This program provides the general functions that are used in the reversi game.
The AI control functions are included in a separate file "AI.py". When called
by "model.py" module, it returns the corresponding results that are needed by
the game model.

"""

__author__ = "Tiansong Cui"
__email__ = "tcui@usc.edu"

def Check_Location(current_table, side, x_ref, y_ref):
    """Check whether it is legal to place a piece at a given location.
        
    According to the reversi game rule, a legal position is a position that
    there exists at least one straight (horizontal, vertical, or diagonal)
    occupied line between the new piece and another piece of the same side,
    with one or more contiguous pieces from the opposite side between them.
    

    Args:
        current_table (2D array): 8*8 values indicating the current condition
                                  of the board.
        side (int): 1 if it is the black side to play, -1 if it is the
                    write side to play.
        x_ref: x coordinate of the given location.
        y_ref: y coordinate of the given location.
    
    Returns:
        Return True if the given location is legal, otherwise return False.

    """
    
    # when the given location is already occupied, we cannot place a piece
    if current_table[x_ref][y_ref] != 0:
        return False
    
    # 8 directions
    dx = [-1, 0, 1, -1, 1, -1, 0, 1]
    dy = [-1, -1, -1, 0, 0, 1, 1, 1]
    
    for k in range(8):
        x = x_ref + dx[k]
        y = y_ref + dy[k]
        
        # whether there is a piece of the other side
        flag = False 
        
        while x >= 0 and x < 8 and y >= 0 and y < 8:
            if current_table[x][y] == 0:
                break
            elif current_table[x][y] != side:
                flag = True
                x += dx[k]
                y += dy[k]
            else:
                if flag:
                    return True
                else:
                    break
    
    return False


def Get_Available_Table(current_table, side, available_table):
    """Get all available locations.

    Args:
        current_table (2D array): 8*8 values indicating the current condition
                                  of the board.
        side (int): 1 if it is the black side to play, -1 if it is the
                    write side to play.
        available_table (2D array): Identify locations that are possible to
                                    place the piece. Modified in place.
    
    Returns:
        flag (bool): Return True if there is at least one available location,
                     otherwise return False.

    """
    
    flag = False

    for i in range(8):
        for j in range(8):
            available_table[i][j] = Check_Location(current_table, side, i, j)
            flag = flag or available_table[i][j]

    return flag


def Move_Piece(current_table, location, direction):
    """Move the piece based on the given direction.
        
    When the player presses <up>, <down>, <left> or <right> on the,
    keyboard, the piece should make the corresponding movement.
    In this function, the 2D movement problem is transformed to a 1D movement
    problem to improve user experience.

    Args:
        current_table (2D array): 8*8 values indicating the current condition
                                  of the board.
        location (array): x and y coordinates of the movable piece.
        direction (str): "left", "right", "up" or "down".
    
    Returns:
        None. Modify location in place.
        
    """
    
    x = location[0]
    y = location[1]    
    
    # two different ways to look at the 2D array as a 1D array
    if direction in ["up", "down"]:
        x,y = y,x

    val = y * 8 + x
    
    if direction in ["right", "down"]:
        step = 1
    else:
        step = -1
    
    while True:
        val += step
        val %= 64
        
        y = val // 8
        x = val % 8
        
        if direction in ["up", "down"]:
            x,y = y,x
        
        if current_table[x][y] == 0:
            break

    location[:] = [x, y]
        
    return


def Place_Piece(current_table, location, side, update_flag=False):
    """If valid, place the piece at the given location.

    After placing the piece, the current piece turns over flips all pieces
    of the other side lying on a straight line between the new piece and any
    anchoring pieces of the current side.
    
    Args:
        current_table (2D array): 8*8 values indicating the current condition
                                  of the board.
        location (array): x and y coordinates of the movable piece.
        side (int): 1 if it is the black side to play, -1 if it is the
                    write side to play.
        update_flag (bool): update the location of the movable piece, should
                            False when called by AI program.
    
    Returns:
        None. Modify current_table and location in place.
        
    """
    
    x_ref = location[0]
    y_ref = location[1]
    
    if Check_Location(current_table, side, x_ref, y_ref) == False:
        return False
    
    current_table[x_ref][y_ref] = side
    
    # 8 directions
    dx = [-1, 0, 1, -1, 1, -1, 0, 1]
    dy = [-1, -1, -1, 0, 0, 1, 1, 1]
    
    for k in range(8):
        x = x_ref + dx[k]
        y = y_ref + dy[k]
        queue = []
        
        while x >= 0 and x < 8 and y >= 0 and y < 8:
            if current_table[x][y] == 0:
                break
            elif current_table[x][y] != side:
                queue.append((x,y))
                x += dx[k]
                y += dy[k]
            else:
                for i, j in queue:
                    current_table[i][j] = side
                break
    
    # unless all the locations are occupied, update the location of the
    # moveable piece
    if update_flag:
        Move_Piece(current_table, location, "right")
    
    return True


def Get_Current_Table(current_table, file):
    """Get the current condition of the table from the file.

    In the file, "*" stands for empty piece, "B" standards for black piece, and
    "W" stands for white piece.
    
    Args:
        current_table (2D array): 8*8 values indicating the current condition
                                  of the board. Will be updated in place.
        file (array): A list of strings representing the current condition of
                      the table.
    
    Returns:
        count (int): Number of occupied pieces.
        
    """

    count = 0
    for i in range(8):
        for j in range(8):
            if file[i][j] == "B":
                current_table[j][i] = 1
                count += 1
            elif file[i][j] == "W":
                current_table[j][i] = -1
                count += 1
            else:
                current_table[j][i] = 0
    
    return count


def Write_To_File(current_table, side, file, end=False):
    """Write the current condition of the table to a file.

    This function is called either during the game when the player presses
    <Esc> button, or the end-of-game condition is met. If it is the end-of-
    game condition, also write the game results.
    
    Args:
        current_table (2D array): 8*8 values indicating the current condition
                                  of the board. Will be updated in place.
        file (array): A list of strings representing the current condition of
                      the table.
        end (bool): Whether it is the end-of-game condition.
    
    Returns:
        None
        
    """
    
    # first line indicates which player to play next
    # will be used when the player chooses to restore the game
    if side == 1:
        file.write("B\n")
    else:
        file.write("W\n")
    
    # write the current or final board condition
    black_count = 0
    write_count = 0
    for i in range(8):
        for j in range(8):
            if current_table[j][i] == 0:
                file.write("*")
            elif current_table[j][i] == 1:
                file.write("B")
                black_count += 1
            else:
                file.write("W")
                write_count += 1
        file.write("\n")
    
    # write the game results
    if end == True:
        file.write("black score: %d\n" % black_count)
        file.write("write score: %d\n" % write_count)
        if black_count > write_count:
            file.write("black wins\n")
        elif black_count < write_count:
            file.write("write wins\n")
        else:
            file.write("draw game\n")
    
    return