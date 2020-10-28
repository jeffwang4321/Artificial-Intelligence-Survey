# f.py - Jeff Wang - 301309384 - CMPT310
# cd mnt/c/users/17789/desktop/310/HW/f
# python3 a5.py


import random, copy

# Description:   Reset Reversi Board to empty board state
def newBoard():
    tboard = [[" "] * 8, [" "] * 8, [" "] * 8, [" "] * 8, [" "] * 8, [" "] * 8, [" "] * 8, [" "] * 8]
    for i in range(8):
        for j in range(8):
            tboard[i][j] = " "

    # Starting pieces:
    tboard[3][3] = "X"
    tboard[3][4] = "O"
    tboard[4][3] = "O"
    tboard[4][4] = "X"
    return tboard


# Description:   Prints current Reversi Board state
def printBoard(tboard):
    print("    0   1   2   3   4   5   6   7   <-- x row")
    print("  +---+---+---+---+---+---+---+---+")
    for i in range(8):
        print("{} ".format(i), end = "")
        for j in range(8):
            print("| {} ".format(tboard[j][i]), end = "")
        print("|")
        print("  +---+---+---+---+---+---+---+---+")
    print("y column\n")
    return


# Description:   Gets the score by counting the tiles on tboard. Returns a dictionary of "X" and "O" wit score values
def getScore(tboard):
    score = {"X":0 , "O":0}
    for i in range(8):
        for j in range(8):
            if tboard[i][j] == "X":
                score["X"] = score["X"] + 1
            if tboard[i][j] == "O":
                score["O"] = score["O"] + 1
    return score


# Description:   Given the number of options, return valid output from (a\b\c) else loop 
def option(num):
    while True:
        x = input()
        if num == 3:
            if x == "a" or x == "b" or x == "c":
                return x
            else:
                print("Invalid option: Please enter (a/b/c):")
        else:
            if x == "a" or x == "b":
                return x
            else:
                print("Invalid option: Please enter (a/b):")


# Description:   Given board state loop until player enters valid position to play their piece
def player(tboard, turn):
    while True:
        print("  Available board moves {} ".format(', '.join(map(str, getValid(tboard, turn))))) # list avaible moves
        print('  Input format for [x,y] positions are "xy", i.e for position [2,4] input "24"')
        move = input("  Please enter the coordinates for your move: ")
        if len(move) == 2 and move[0] in ["0", "1", "2", "3", "4", "5", "6" , "7"] and move[1] in ["0", "1", "2", "3", "4", "5", "6" , "7"]:
            if checkValid(board, turn, int(move[0]), int(move[1])) == False:
                print("Error: Invalid coordinates\n")
                continue
            else:
                listmove = [int(move[0]), int(move[1])]
                break
        else:
            print("Error: Invalid input format\n")

    return listmove


# Description:   Check that the inputed x & y positions are valid moves on tboard state
def checkValid(tboard, turn, x, y):
    # Return false if the position is already filled or the position is outside the board's range
    if tboard[x][y] != " " or x < 0 or x > 7 or y < 0 or y > 7:
        return False

    # Create variable for the other tile
    if turn == "X":
        otherTurn = "O"
    else:
        otherTurn = "X"

    # Iterate position x,y with all 8 board directions (N, NE, E, SE, S, SW, W, NW)
    for xmove, ymove in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        xtemp, ytemp = x, y
        xtemp = xtemp + xmove
        ytemp = ytemp + ymove

        # if there is a neighboring piece  of the other tile on the board in that x,y direction
        if xtemp >= 0 and xtemp <= 7 and ytemp >= 0 and ytemp <= 7 and tboard[xtemp][ytemp] == otherTurn:
            xtemp = xtemp + xmove
            ytemp = ytemp + ymove
            if xtemp < 0 or xtemp > 7 or ytemp < 0 or ytemp > 7: # Break out if it's outside the board space
                continue

            while tboard[xtemp][ytemp] == otherTurn: # Loop while neighboring piece++ is still on the board
                xtemp = xtemp + xmove
                ytemp = ytemp + ymove
                if xtemp < 0 or xtemp > 7 or ytemp < 0 or ytemp > 7: # Break out if it's outside the board space
                    break

            if xtemp < 0 or xtemp > 7 or ytemp < 0 or ytemp > 7:
                continue

            if tboard[xtemp][ytemp] == turn: # The neighboring pieces ends in our original piece, return true for valid move
                return True

    return False


# Description:   Returns a list of valid positions for tboard state
def getValid(tboard, turn):
    valid = []
    for x in range(8): # iterate tboard and check if each position is valid
        for y in range(8):
            if checkValid(tboard, turn, x, y) != False:
                valid.append([x, y])
    return valid


# Description:   Flip the tiles on tboard state given input position x,y
def flip(tboard, turn, x, y):
    flipy = []

    # Create variable for the other tile
    if turn == "X":
        otherTurn = "O"
    else:
        otherTurn = "X"

    # Iterate position x,y with all 8 board directions (N, NE, E, SE, S, SW, W, NW)
    for xmove, ymove in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        xtemp, ytemp = x, y
        xtemp = xtemp + xmove
        ytemp = ytemp + ymove

        # if there is a neighboring piece  of the other tile on the board in that x,y direction
        if xtemp >= 0 and xtemp <= 7 and ytemp >= 0 and ytemp <= 7 and tboard[xtemp][ytemp] == otherTurn:
            xtemp = xtemp + xmove
            ytemp = ytemp + ymove
            if xtemp < 0 or xtemp > 7 or ytemp < 0 or ytemp > 7: # Break out if it's outside the board space
                continue

            while tboard[xtemp][ytemp] == otherTurn: # Loop while neighboring piece++ is still on the board
                xtemp = xtemp + xmove
                ytemp = ytemp + ymove
                if xtemp < 0 or xtemp > 7 or ytemp < 0 or ytemp > 7: # Break out if it's outside the board space
                    break

            if xtemp < 0 or xtemp > 7 or ytemp < 0 or ytemp > 7:
                continue

            if tboard[xtemp][ytemp] == turn: # The neighboring pieces ends in our original piece, return ture for valid move
                while True: # iterate backwards and append all other tiles in between that needs to be flip
                    xtemp = xtemp - xmove
                    ytemp = ytemp - ymove
                    if xtemp == x and ytemp == y:
                        break
                    flipy.append([xtemp, ytemp])

    tboard[x][y] = turn # Set the x,y tile on the board
    for i, j in flipy:  # flip all the tiles in between in the list of tiles to be flipped
        tboard[i][j] = turn
    return tboard


# Description:   Returns the best move possible for the computer from tboard state, using Pure MCTS random moves and maximun Win/Loss/Tie score statistic (Win: +1) (Loss: -1)
def mctsMove(tboard, turn):
    # Save the list of value moves for tboard state's first move as a dictionary for win/loss statistics later
    firstlist = getValid(tboard, turn)
    d = {}
    for j in firstlist:
        d[str(j)] = 0

    # Generating 300 random games from current tboard position
    for j in range(300):

        tempboard = copy.deepcopy(tboard) # Copy board to temp board, and turn to tempturn
        tempturn = turn

        if turn == "X": # Create variable for the other tile
            otherTurn = "O"
        else:
            otherTurn = "X"

        i = 0
        while True: # For loop from current turn to end game
            if getValid(tempboard, tempturn) == []:
                score = getScore(tempboard)
                if score[otherTurn] > score[turn]: # increment dictionary on a win and decrement on a loss
                    d[str(firstmove)] = int(d[str(firstmove)]) - 1
                elif score[otherTurn] < score[turn]:
                    d[str(firstmove)] = int(d[str(firstmove)]) + 1
                break

            tempmove = random.choice(getValid(tempboard, tempturn)) # Generating a random move for tempboard and flip
            tempboard = flip(tempboard, tempturn, tempmove[0], tempmove[1])

            if i == 0:  # Saving firstmove for Win/Loss/Tie tracking later
                firstmove = tempmove

            # Change to other tile for next computer turn
            if tempturn == "O":
                tempturn = "X"
            else:
                tempturn = "O"
            i = i + 1

    # Check for maximun Win/Loss/Tie score from dictionary statistics, return hightest score move
    max = -301
    index = []
    for i in d:
        if int(d[i]) > max :
            max = int(d[i])
            index = [int(i[1]), int(i[4])]

    return index


# Description:   Returns the best move possible for the computer from tboard state, using MCTS + corner capturing + mobility scoring + different scoring heuristic
def mctsMove2(tboard, turn):
    # Save the list of value moves for tboard state's firstmove as a dictionary for win/loss statistics later
    firstlist = getValid(tboard, turn)
    d = {}
    for j in firstlist:
        d[str(j)] = 0

    # Prioritize capturing corner if available
    for x in firstlist:
        if x in [[0, 0], [7, 0], [0, 7], [7, 7]]:
            return x

    # Generating 300 games from current tboard position
    for j in range(300):

        tempboard = copy.deepcopy(tboard) # Copy board to temp board, and turn to tempturn
        tempturn = turn

        if turn == "X": # Change to other tile for next computer turn
            otherTurn = "O"
        else:
            otherTurn = "X"

        i = 0
        while True: # For loop from current turn to end game
            if getValid(tempboard, tempturn) == []: # if no more valid moves (Game Over) then increment dictionary by the difference between their score
                score = getScore(tempboard)
                d[str(firstmove)] = int(d[str(firstmove)]) + score[turn] - score[otherTurn]
                break

            tempmove = random.choice(getValid(tempboard, tempturn)) # Generating a random move for temp board and flip
            tempboard = flip(tempboard, tempturn, tempmove[0], tempmove[1])

            if i == 0:  # Saving firstmove for Win/Loss/Tie tracking later
                firstmove = tempmove
                d[str(firstmove)] = int(d[str(firstmove)]) + len(getValid(tempboard, tempturn)) # additional scoring heuristic for extra mobility on first move


            # Change turn to other computer turn
            if tempturn == "O":
                tempturn = "X"
            else:
                tempturn = "O"
            i = i + 1

    # Check for maximun Win/Loss/Tie score from dictionary statistics, return hightest score move
    max = -100000
    index = []
    for i in d:
        if int(d[i]) > max :
            max = int(d[i])
            index = [int(i[1]), int(i[4])]

    return index



# Main function
if __name__ == "__main__":
    # loops until quit game
    while True:
        # initialize input option for piece X
        print("\nWelcome to Jeff Wang's CMPT310 Final Project Reversi")
        print("  Please select an input option for piece X (a/b/c): ")
        print("    a) User manually input")
        print("    b) Computer AI using Pure Monte-Carlo Tree Search")
        print("    c) Computer AI using Monte-Carlo Tree Search and best move heuristics")
        xinput = option(3)

        # initialize input option for piece O
        print("  Please select an input option for piece O (a/b/c): ")
        print("    a) User manually input")
        print("    b) Computer AI using Pure Monte-Carlo Tree Search (MCTS)")
        print("    c) Computer AI using Monte-Carlo Tree Search and best move heuristics")
        oinput = option(3)

        # initialize turn
        print("  Please select a which piece moves first? (a/b): ")
        print("    a) Piece X")
        print("    b) Piece O")
        if option(2) == "a":
            turn = "X"
        else:
            turn = "O"

        board = newBoard() # create new board and print
        printBoard(board)

        # loops through 1 game
        while True:

            # Check for game over (if there are no valid moves available)
            if getValid(board, turn) == []:
                print("***Game Over***")
                score = getScore(board) # Get the score from board state
                print("  X score:", score["X"], ", O score:", score["O"])
                if score["X"] == score["O"]: # Tie game
                    print("  Tie Game!")

                elif score["X"] > score["O"]: # Print O input option wins
                    if xinput == "a": # Print X input option wins
                        print("  Player X Wins!")
                    elif xinput == "b":
                        print("  Pure MCTS AI X Wins!")
                    else:
                        print("  MCTS & Heuristics AI X Wins!")
                else:
                    if oinput == "a":
                        print("  Player O Wins!")
                    elif oinput == "b":
                        print("  Pure MCTS AI O Wins!")
                    else:
                        print("  MCTS & Heuristics AI O Wins!")

                break

            # Check if it's X's turn or O's turn
            if turn == "X":
                if xinput == "a": # Check input method X is player, AI 1 or AI 2
                    print("Player X's turn.")
                    listmove = player(board, turn)
                elif xinput == "b":
                    print("Pure MCTS AI X's turn.")
                    listmove = mctsMove(board, turn)
                else:
                    print("MCTS & Heuristics AI X's turn.")
                    listmove = mctsMove2(board, turn)

            else:
                if oinput == "a": # Check input method O is player, AI 1 or AI 2
                    print("Player O's turn.")
                    listmove = player(board, turn)
                elif oinput == "b":
                    print("Pure MCTS AI O's turn.")
                    listmove = mctsMove(board, turn)
                else:
                    print("MCTS & Heuristics AI O's turn.")
                    listmove = mctsMove2(board, turn)

            # Given listmove value flip board pieces and print new board state
            board = flip(board, turn, listmove[0], listmove[1])
            print("Chosen position: {}\n".format(listmove))
            printBoard(board);

            # Change turn to other piece and repeat loop
            if turn == "O":
                turn = "X"
            else:
                turn = "O"

        # Option to play again
        print("\nDo you want to play again? (a/b): ")
        print("  a) Yes")
        print("  b) No")
        if option(2) == "a":
            continue
        else:
            exit()
