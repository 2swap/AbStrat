
import time, random

boardheight = 6
boardwidth = 7
steadystates = [
        [
        list("*      "),
        list("-**  **"),
        list("*--2 --"),
        list("-**1*1*"),
        list("*--2-2-"),
        list("- 12 21")
        ],
        [
        list("*** ***"), # The original! This works!
        list("---2---"),
        list("***1***"),
        list("---2---"),
        list("**11*+ "),
        list("--21-2+")
        ],
        [
        list("**     "), # Woah...
        list("--     "),
        list("* 1****"),
        list("-12--++"),
        list(" 21**  "),
        list("212--++")
        ],
        [
        list("** ****"),
        list("--2-*--"),
        list("*11*-**"),
        list("-22----"),
        list("+21**  "),
        list("112--++")
        ],
        [
        list("** ****"),
        list("--1----"),
        list("**1+***"),
        list("--2+---"),
        list("**12***"),
        list("--21--2")
        ],
        [
        list("**-*-*-"),
        list("-+*-*-*"),
        list("* +1-2-"),
        list("-+ 1*1 "),
        list("* +2-22"),
        list("-+12 21")
        ]

]

def generate_board():
    steadystate =[
        list("*--1***"),
        list("-**2---"),
        list("*--1***"),
        list("+**2---"),
        list("*-+12**"),
        list("- 221--")
        ]
    board = [1]*boardheight
    for i in range(boardheight):
        board[i] = ["."]*boardwidth
    for x in range(boardwidth):
        for y in range(boardheight):
            board[y][x] = steadystate[y][x]
    for x in range(boardwidth):
        for y in range(boardheight):
            if board[y][x] != "1" and board[y][x] != "2":
                board[y][x] = "."
    return (steadystate, board)

def print_board(board):
    print("\n")
    for row in board:
        print(" ".join(row))
    print("\n")
    print(" ".join(["1","2","3","4","5","6","7"]))
    print("\n")
 
def mark_board(steadystate, board, last, column, player):
    p = str(player)
    board[last][column] = p
    steadystate[last][column] = p

def play(steadystate, board):
    #column = int(input("Pick a column (1-7): ")) - 1
    column = random.randint(0,6)
    while board[0][column] != ".":
        column = random.randint(0,6)
    for i in range(boardheight):
        if board[i][column] == ".":
            last = i
    mark_board(steadystate, board, last, column, 1)

def steadystateresponse(steadystate):
    """
    alph = {}
    column = -1
    for x in range(boardwidth):
        for y in range(boardheight):
            letter = steadystate[y][x]
            alph[letter] = alph.get(letter, 0) + 1
    for key in alph:
        if alph[key] == 1:
            for x in range(boardwidth):
                for y in range(boardheight):
                    if steadystate[y][x] == key:
                        column = x
    """

    priorities = ["x"]*boardwidth
    for x in range(boardwidth):
        for y in range(boardheight):
            ss = steadystate[y][x]
            if ss != "1" and ss != "2":
                priorities[x] = ss

    print(priorities)

    column = -1
    for x in ["*", "+", " ", "-"]:
        if x in priorities:
            column = priorities.index(x)
            break

    for i in range(boardheight):
        if board[i][column] == ".":
            last = i
    mark_board(steadystate, board, last, column, 2)

def check_winner(board, player):
    #check horizontal spaces
    for y in range(boardheight):
        for x in range(boardwidth - 3):
            if board[y][x] == player and board[y][x+1] == player and board[y][x+2] == player and board[y][x+3] == player:
                return True

    #check vertical spaces
    for x in range(boardwidth):
        for y in range(boardheight - 3):
            if board[y][x] == player and board[y+1][x] == player and board[y+2][x] == player and board[y+3][x] == player:
                return True

    #check / diagonal spaces
    for x in range(boardwidth - 3):
        for y in range(3, boardheight):
            if board[y][x] == player and board[y-1][x+1] == player and board[y-2][x+2] == player and board[y-3][x+3] == player:
                return True

    #check \ diagonal spaces
    for x in range(boardwidth - 3):
        for y in range(boardheight - 3):
            if board[y][x] == player and board[y+1][x+1] == player and board[y+2][x+2] == player and board[y+3][x+3] == player:
                return True

    return False



winner = False
wins = 0
loses = 0
while True:
    (steadystate, board) = generate_board()
    while True:
        play(steadystate, board)
        print_board(board)
        if check_winner(board, "1"):
            loses+=1
            print("You win!")
            print(str(wins) + " " + str(loses))
            exit()
        steadystateresponse(steadystate)
        print_board(board)
        if check_winner(board, "2"):
            wins+=1
            print("You lose!")
            print(str(wins) + " " + str(loses))
            break


