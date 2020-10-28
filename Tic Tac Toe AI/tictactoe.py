# a3.py - Jeff Wang - 301309384 - CMPT310
# cd mnt/c/users/17789/desktop/310/HW/a3
# python3 a3.py


import random, copy


# Global Tic-Tac-Toe Board variable implemented using dictionary, initialized to blanks spaces
board = {1: ' ' , 2: ' ' , 3: ' ' , 4: ' ' , 5: ' ' , 6: ' ' , 7: ' ' , 8: ' ' , 9: ' ' }


# Description:   Reset board to empty board state
def reset():
    global board
    board = {1: ' ' , 2: ' ' , 3: ' ' , 4: ' ' , 5: ' ' , 6: ' ' , 7: ' ' , 8: ' ' , 9: ' ' }


# Description:   Prints current Tic-Tac-Toe Board state
def printboard(tboard):
    print("", tboard[1], '|', tboard[2], '|', tboard[3])
    print('---+---+---')
    print("", tboard[4], '|', tboard[5], '|', tboard[6])
    print('---+---+---')
    print("", tboard[7], '|', tboard[8], '|', tboard[9], "\n")


# Description:   Prints the Tic-Tac-Toe positions that map to the Tic-Tac-Toe Board
def printpositions():
    print("\nTic-Tac-Toe Positions:")
    print(" 1 | 2 | 3")
    print('---+---+---')
    print(" 4 | 5 | 6")
    print('---+---+---')
    print(" 7 | 8 | 9\n")


# Description:   Returns a random legal move for tboard state
def randmove(tboard):
    rand = random.randint(1, 9)
    while tboard[rand] != ' ':
        rand = random.randint(1, 9)
    return rand


# Description:   Returns the best move possible for the computer from tboard state, using the maximun Win/Loss/Tie score statistic
#                (Win: +10, +Bonus for less moves/ win fast) (Loss: -10, +Bonus for extra moves/ delaying loss)
def bestmove(turncount, tboard):
    # Temparray is a dictionary that will store Win/Loss/Tie score statistics
    temparray = {1: ' ' , 2: ' ' , 3: ' ' , 4: ' ' , 5: ' ' , 6: ' ' , 7: ' ' , 8: ' ' , 9: ' ' }

    # Generating 1000 random games from current tboard position
    for j in range(1000):

        tempboard = copy.deepcopy(tboard) # Copy board to temp board
        tempturn = "O"

        for i in range(turncount, 9): # For loop from current turn to tie game/ tie game

            tempmove = randmove(tempboard) # Generating a random move for temp board
            tempboard[tempmove] = tempturn

            if i == turncount:  # Saving firstmove for Win/Loss/Tie tracking later
                firstmove = tempmove

            # Create T/F variables to check for wins
            row1 = tempboard[1] == tempboard[2] == tempboard[3] != ' '   # Won across the top row
            row2 = tempboard[4] == tempboard[5] == tempboard[6] != ' '   # Won across the middle row
            row3 = tempboard[7] == tempboard[8] == tempboard[9] != ' '   # Won across the bottom row
            down1 = tempboard[1] == tempboard[4] == tempboard[7] != ' '  # Won down the left column
            down2 = tempboard[2] == tempboard[5] == tempboard[8] != ' '  # Won down the middle column
            down3 = tempboard[3] == tempboard[6] == tempboard[9] != ' '  # Won across the right column
            diag1 = tempboard[1] == tempboard[5] == tempboard[9] != ' '  # Won down the right diagonal
            diag2 = tempboard[3] == tempboard[5] == tempboard[7] != ' '  # Won down the left diagonal

            # Check if Computer O has won or loss with the randomly generated moves
            if row1 or row2 or row3 or down1 or down2 or down3 or diag1 or diag2: # Won across the top

                # Initialize temparray to 0 on the first hit for Win/Loss/Tie statistics
                if temparray[firstmove] == ' ':
                    temparray[firstmove] = '0'

                # Set the score for that first move if it lead to a (Win: +10, +Bonus for less moves/ win fast) (Loss: -10, +Bonus for extra moves/ delaying loss)
                if tempturn == "O":
                    temparray[firstmove] = str(int(temparray[firstmove]) + 10 + 8 - i)
                else:
                    temparray[firstmove] = str(int(temparray[firstmove]) - 10 - 8 + i)
                break

            # Full board with no wins, it's a tie, initialize temparray to 0 on the first tie for Win/Loss/Tie statistics
            if i == 8:
                if temparray[firstmove] == ' ':
                    temparray[firstmove] = '0'

            # Change turn to other computer turn
            if tempturn == "O":
                tempturn = "X"
            else:
                tempturn = "O"

    # Check for maximun Win/Loss/Tie score from our temparray statistics
    max = -1000
    index = 0
    for i in temparray:
        # print(i, ": ", temparray[i])     #Print Win/Loss/Tie score after 1000 games
        if temparray[i] != ' ' and int(temparray[i]) > max :
            max = int(temparray[i])
            index = i

    if index == 0:
        return randmove(tboard)

    return index # Return index with max score


# Description:   Play a new game against a computer
def play_a_new_game():

    printpositions()
    print("Welcome to Tic-Tac-Toe vs Computer")
    check = input("Does the player want to go first? (y/n): ")

    # Check if player is going first or computer is going first
    if check == "y" or check == "Y":
        print("Player X is going first!\n")
        turn = "X"
    else:
        print("Computer O is going first!\n")
        turn = "O"


    for i in range(9):
        printboard(board)

        # Check if it's Player's turn to input a move or Computer's turn to generate a best move
        if turn == "X":
            print("Player X's turn." )
            move = input("Choose a position from 1 - 9: ")
        else:
            print("Computer O's turn." )
            move = str(bestmove(i, board))
            print("Choose a position from 1 - 9: ", move)


        # Check if players move is vaild for the board state
        repeat = True
        while repeat:
            # Check for vaild integer
            while move not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                move = input("Choose a position from 1 - 9: ")
            move = int(move)

            # Check for valid empty position
            if board[move] == ' ':
                board[move] = turn
                repeat = False
            else:
                print("***That position is already filled!***\n")
                repeat = True

        # Create T/F variables to check for wins
        row1 = board[1] == board[2] == board[3] != ' '   # Won across the top row
        row2 = board[4] == board[5] == board[6] != ' '   # Won across the middle row
        row3 = board[7] == board[8] == board[9] != ' '   # Won across the bottom row
        down1 = board[1] == board[4] == board[7] != ' '  # Won down the left column
        down2 = board[2] == board[5] == board[8] != ' '  # Won down the middle column
        down3 = board[3] == board[6] == board[9] != ' '  # Won across the right column
        diag1 = board[1] == board[5] == board[9] != ' '  # Won down the right diagonal
        diag2 = board[3] == board[5] == board[7] != ' '  # Won down the left diagonal

        # Check if the Player or Computer has won
        if row1 or row2 or row3 or down1 or down2 or down3 or diag1 or diag2:
            printboard(board)
            if turn == "X":
                print("***Player X won!***")
            else:
                print("***Computer O won!***")
            break

        # Change turn to other player if nobody won
        if turn == "O":
            turn = "X"
        else:
            turn = "O"

        # Check for full board with no wins, therefore it's a tie
        if i == 8:
            printboard(board)
            print("***Tie game!***")


    # Option to play again, reset game to blank board state
    restart = input("Do want to play again? (y/n): ")
    if restart == "y" or restart == "Y":
        reset()
        play_a_new_game()


# Main function
if __name__ == "__main__":
    play_a_new_game()
