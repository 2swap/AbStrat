from pprint import pprint
import time, random

boardheight = 6
boardwidth = 7
priority_list = ["+", " ", "-"]
miai = ['@','#', '$']
steadystates = [[
        list("+-+@-#-"),
        list("-+-2+1+"),
        list("+-21-2-"),
        list("-+12+1+"),
        list("$-21-2-"),
        list("2@12$1#")
]]*1000
ssindex = 0
known_steadystates = [
        [
        list("+++c+++"), # The original!
        list("---2---"),
        list("+++1+++"),
        list("---2---"),
        list("++11+ad"),
        list("--21-2b")
        ],
        [
        list("*******"), # woah...
        list("-------"),
        list("*#1****"),
        list("-12--++"),
        list("#21**  "),
        list("212--@@")
        ],
        [
        list("++111++"), # First found computationally!
        list("-+222+-"),
        list("++112-+"),
        list("--221+-"),
        list("++112-+"),
        list("--221+2")
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
        list("+ 1+- *"),
        list("--2 +* "),
        list("+11 *+*"),
        list("*222*+*"),
        list("-211-* "),
        list("1122 -+")
        ],
        [
        list("   2++ "), # good but not perfect
        list("  -2*1 "),
        list("+ 21-2 "),
        list("-*12+1*"),
        list("+-21-2-"),
        list("2112+1+")
        ]
]

def generate_board():
    board = [1]*boardheight
    ss = [1]*boardheight
    for i in range(boardheight):
        board[i] = ["."]*boardwidth
        ss[i] = ["."]*boardwidth
    for x in range(boardwidth):
        for y in range(boardheight):
            board[y][x] = steadystates[ssindex][y][x]
            ss[y][x] = steadystates[ssindex][y][x]
    for x in range(boardwidth):
        for y in range(boardheight):
            if board[y][x] not in ["1", "2"]:
                board[y][x] = "."
    return (ss, board)

def print_board(board):
    print("\n")
    for row in board:
        print(" ".join(row))
    print("\n")
    print(" ".join(["1","2","3","4","5","6","7"]))
    print("\n")
 
def mark_board(steadystate, board, y, x, player):
    p = str(player)
    board[y][x] = p
    steadystate[y][x] = p

def play(steadystate, board):
    #column = int(input("Pick a column (1-7): ")) - 1
    x = -1
    indices = [i for i, x in enumerate(board[0]) if x == '.'] # get indices of all legal moves
    if indices: # if there is a legal move
        x = random.choice(indices) # choose a random index from the list of indices
    else:
        return False # There are no legal moves.
    for y in range(boardheight-1,-1,-1):
        if board[y][x] == ".":
            mark_board(steadystate, board, y, x, 1)
            return True
    return False

def steadystateresponse(steadystate):
    alph = {}
    for x in range(boardwidth):
        for y in range(boardheight):
            letter = steadystate[y][x]
            if letter in miai:
                alph[letter] = alph.get(letter, 0) + 1
    for key in alph:
        if alph[key] > 2:
            return False
        if alph[key] == 1:
            for x in range(boardwidth):
                for y in range(boardheight):
                    if steadystate[y][x] == key:
                        if y!=boardheight-1 and board[y+1][x]=='.':
                            return False
                        mark_board(steadystate, board, y, x, 2)
                        return True
            return False

    priorities = ["x"]*boardwidth
    for x in range(boardwidth):
        for y in range(boardheight):
            ss = steadystate[y][x]
            if ss != "1" and ss != "2":
                priorities[x] = ss

    x = -1
    for i in priority_list:
        if i in priorities:
            x = priorities.index(i)
            break

    y = -1
    for i in range(boardheight):
        if board[i][x] == ".":
            y = i
    if y == -1 or x == -1:
        return False
    mark_board(steadystate, board, y, x, 2)
    return True

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

def onwin(ssindex):
    whichoverwrite = random.randint(0,len(steadystates)-1)
    while whichoverwrite == ssindex:
        whichoverwrite = random.randint(0,len(steadystates)-1)
    r = random.random()
    if r < 0.2:
        y = random.randint(0, boardheight-1)
        x = random.randint(0, boardwidth-1)
        steadystates[whichoverwrite][y][x] = steadystates[ssindex][y][x]
    elif r<0.25:
        steadystates[whichoverwrite] = mutate(steadystates[ssindex])

def mutate(ss):
    (ret,_) = generate_board()
    for y in range(boardheight):
        for x in range(boardwidth):
            if ret[y][x] in priority_list and random.random()<0.05:
                ret[y][x] = random.choice(priority_list + miai)
    return ret

while True:
    ssindex = random.randint(0,len(steadystates)-1)
    wins = 0
    while True:
        (steadystate, board) = generate_board()
        won = False
        while True:
            if not play(steadystate, board):
                break
            if check_winner(board, "1"):
                break
            if not steadystateresponse(steadystate):
                break
            if check_winner(board, "2"):
                wins+=1
                won = True
                if wins % 1000 == 0:
                    print(f"SteadyState wins! {wins}")
                if wins % 10000 == 0:
                    pprint(steadystates[ssindex])
                if wins == 100000:
                    exit()
                onwin(ssindex)
                break
        if not won:
            print(f"wins: {wins}")
            break

