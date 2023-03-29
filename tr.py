import random

board = []
hashlist = {}

sz = 5
turn='v'

def board_heuristic(b):
    if b[1][4] == '>' and b[2][4] == '>' and b[3][4] == '>':
        return -1
    if b[4][1] == 'v' and b[4][2] == 'v' and b[4][3] == 'v':
        return 1
    return 0

def minimax(b, who):
    strb = str(b)+who

    if strb in hashlist.keys():
        return hashlist[strb]

    heur = board_heuristic(b)
    if heur != 0:
        return heur

    if who=='v':
        value = -2
        for i in range(3):
            child = move(b, 'v', i)
            if child != False:
                minicld = minimax(child, '>')
                value = max(value, minicld)
        hashlist[strb] = value
    else:
        value = 2
        for i in range(3):
            child = move(b, '>', i)
            if child != False:
                minicld = minimax(child, 'v')
                value = min(value, minicld)
        hashlist[strb] = value
    return hashlist[strb]

def printboard(b):
    print("         1   2   3      ");
    print("   +---+---+---+---+---+")
    for i in range(sz):
        print(" "+str(i)+" " if i>0 and i!=sz-1 else "    ", end="")
        for j in range(sz):
            print("| " + b[i][j] + " ", end="")
        print("|")
        print("   +---+---+---+---+---+")
    print()
    print()

def move(b, t, mv):
    newBoard = [row[:] for row in b]
    if mv < 0 or mv > sz-2:
        return false
    spot = mv + 1
    caught = -1
    caughtSpot = -1
    for i in range(sz):
        rowcol = (spot, i) if t=='>' else (i, spot)
        if caught>=0 and caught<sz and i-caught<3 and newBoard[rowcol[0]][rowcol[1]]==' ':
            newBoard[caughtSpot[0]][caughtSpot[1]] = ' '
            newBoard[rowcol[0]][rowcol[1]] = t
            return newBoard
        if newBoard[rowcol[0]][rowcol[1]] == t:
            caught = i
            caughtSpot = rowcol
    return False

for i in range(sz):
    board.append([])
    for j in range(sz):
        board[i].append(' ')

empty = [row[:] for row in board]
empty[1][4] = '>'
empty[2][3] = '>'
empty[3][4] = '>'
empty[4][1] = 'v'
empty[3][2] = 'v'
empty[4][3] = 'v'
assert minimax(empty, 'v') == 1
empty[4][2] = 'v'
empty[3][2] = ' '
assert minimax(empty, 'v') == 1
assert minimax(empty, '>') == 1

for i in range(1, sz-1):
    board[0][i] = 'v'
    board[i][0] = '>'


printboard(board)
while(True):
    print(minimax(board, turn))
    if turn == 'v':
        mv = int(input(turn + " to move: "))-1
    else:
        ok = []
        for i in range (3):
            cld = move(board, '>', i)
            if cld != False and minimax(cld, 'v') < 0:
                ok.append(i)
        mv = random.choice(ok)
    newBoard = move(board, turn, mv)
    if newBoard != False:
        board = newBoard
        turn = '>' if turn=='v' else 'v'
    else:
        print("ERROR!!")
    printboard(board)

