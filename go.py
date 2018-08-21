"""
I implement a functioning 9x9 Go board that follows the rules of capture and ko. The game will end when both players pass.
Scoring is manual.
"""

board = []
board.append([" "]+["1","2","3","4","5","6","7","8","9"]+["X"])
for i in range(1,10):
    board.append([str(i)]+["O"]*9+["X"])
board.append(["X"]*11)

def board_print(board):
    for i in range(10):
        print(" ".join(board[i][0:10]))

def adjacency_set(board,row,column):
    return([board[row-1][column],board[row+1][column],board[row][column-1],board[row][column+1]])

already_checked = []
purgatory = []
def capture_check(board,row,column,colour):
    if "O" in adjacency_set(board,row,column):
        return False
    else:
        already_checked.append([row,column])
        purgatory.append([row,column])
        if board[row-1][column] == colour and [row-1,column] not in already_checked:
            if not capture_check(board,row-1,column,colour):
                return False
        if board[row+1][column] == colour and [row+1,column] not in already_checked:
            if not capture_check(board,row+1,column,colour):
                return False
        if board[row][column-1] == colour and [row,column-1] not in already_checked:
            if not capture_check(board,row,column-1, colour):
                return False
        if board[row][column+1] == colour and [row,column+1] not in already_checked:
            if not capture_check(board,row,column+1, colour):
                return False
    return True

def board_refresh_B(board,row,column):
    if board[row-1][column] == "W":
        already_checked = []
        if capture_check(board,row-1,column,"W"):
            for stone in purgatory:
                board[stone[0]][stone[1]] = "O"
    if board[row+1][column] == "W":
        already_checked = []
        if capture_check(board,row+1,column,"W"):
            for stone in purgatory:
                board[stone[0]][stone[1]] = "O"
            board_print(board)
    if board[row][column-1] == "W":
        already_checked = []
        if capture_check(board,row,column-1,"W"):
            for stone in purgatory:
                board[stone[0]][stone[1]] = "O"
    if board[row][column+1] == "W":
        already_checked = []
        if capture_check(board,row,column+1,"W"):
            for stone in purgatory:
                board[stone[0]][stone[1]] = "O"
    return board

def board_refresh_W(board,row,column):
    if board[row-1][column] == "B":
        already_checked = []
        if capture_check(board,row-1,column,"B"):
            for stone in purgatory:
                board[stone[0]][stone[1]] = "O"
    if board[row+1][column] == "B":
        already_checked = []
        if capture_check(board,row+1,column,"B"):
            for stone in purgatory:
                board[stone[0]][stone[1]] = "O"
            board_print(board)
    if board[row][column-1] == "B":
        already_checked = []
        if capture_check(board,row,column-1,"B"):
            for stone in purgatory:
                board[stone[0]][stone[1]] = "O"
    if board[row][column+1] == "B":
        already_checked = []
        if capture_check(board,row,column+1,"B"):
            for stone in purgatory:
                board[stone[0]][stone[1]] = "O"
    return board

print('Instructions: To play a move, enter its numeric coordinates separated by a space. The input should be a string.')
pass_B = False
pass_W = False
previous_state_B = []
previous_state_W = []
board_print(board)
while not (pass_B and pass_W):
    move_valid = False
    while not move_valid:
        print("Black's move. To pass, type 'pass'.")
        try:
            row, column = map(int, input().split())
        except ValueError:
            pass_B = True
            break
        if board[row][column] != "O":
            print("There is already a stone there. Choose another move.")
        else:
            board_save = map(tuple,board)
            board[row][column] = "B"
            #check board state
            already_checked[:] = []
            purgatory[:] = []
            if capture_check(board_refresh_B(board,row,column),row,column,"B"):
                print("Illegal move. Choose another move.")
                board[row][column] = "O"
            elif board_refresh_B(board,row,column) == map(list,previous_state_B):
                print("Ko violation. Choose another move.")
                board = map(list,board_save)
            else:
                already_checked[:] = []
                purgatory[:] = []
                move_valid = True
                board = board_refresh_B(board,row,column)
                previous_state_B = map(tuple,board)
                board_print(board)


    move_valid = False
    while not move_valid:
        print("White's move")
        try:
            row, column = map(int, input().split())
        except ValueError:
            pass_W =  True
            break
        if board[row][column] != "O":
            print("There is already a stone there. Choose another move.")
        else:
            board_save = map(tuple,board)
            board[row][column] = "W"
            # check board state
            already_checked[:] = []
            purgatory[:] = []
            if capture_check(board_refresh_W(board,row,column),row,column,"W"):
                print("Illegal move. Choose another move.")
                board[row][column] = "O"
            elif board_refresh_W(board,row,column) == map(list,previous_state_W):
                print("Ko violation. Choose another move.")
                board = map(list,board_save)
            else:
                already_checked[:] = []
                purgatory[:] = []
                move_valid = True
                board = board_refresh_W(board,row,column)
                previous_state_W = map(tuple,board)
                board_print(board)

print("Both players have passed. Game over.")
print("Final board position:")
board_print(board)

