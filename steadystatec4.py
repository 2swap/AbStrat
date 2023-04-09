from pprint import pprint
import copy
import time, random

known_steadystates = [
        [
        list("   -   "),
        list("   2   "),
        list("   1   "),
        list("   2   "),
        list("  11 =-"),
        list("  21 2+")
        ],
        [
        list("  #    "),
        list("  1    "),
        list("  1  ++"),
        list("  2  =="),
        list("#21  --"),
        list("212  @@")
        ],
        [
        list("       "),
        list("       "),
        list(" #1  ++"),
        list(" 12  =="),
        list("#21  --"),
        list("212  @@")
        ],
        [
        list("  111+ "),
        list("  222+ "),
        list("  112+ "),
        list("  221+ "),
        list("  112+ "),
        list("  221+2")
        ],
        [
        list("  ##   "),
        list("  12   "),
        list("  11   "),
        list("  21   "),
        list("  12  2"),
        list("  21  2")
        ],
        [
        list(" @+    "),
        list(" 11    "),
        list(" 21    "),
        list(" 22    "),
        list("@21    "),
        list("112 2  ")
        ],
        [
        list(" -     "),
        list(" 1     "),
        list(" 21    "),
        list(" 22    "),
        list("121    "),
        list("112 2  ")
        ],
        [
        list("   -   "),
        list("   =   "),
        list("   +   "),
        list("   2   "),
        list("  11 =="),
        list("  21 2=")
        ],
]

unproven=[
        [
        list("       "),
        list("   2 1 "),
        list("  21 2 "),
        list("  12 1 "),
        list("  21 2 "),
        list("2 12 1 ")
        ],
        [
        list("   2++ "), # good but not perfect
        list("  -2*1 "),
        list("+ 21-2 "),
        list("-*12+1*"),
        list("+-21-2-"),
        list("2112+1+")
        ],
]

boardheight = 6
boardwidth = 7
priority_list = ["+", "=", "-"]
miai = ['@','#']

def generate_board(steadystate):
    board = [1]*boardheight
    ss = [1]*boardheight
    for i in range(boardheight):
        board[i] = ["."]*boardwidth
        ss[i] = ["."]*boardwidth
    for x in range(boardwidth):
        for y in range(boardheight):
            board[y][x] = steadystate[y][x]
            ss[y][x] = steadystate[y][x]
    for x in range(boardwidth):
        for y in range(boardheight):
            if board[y][x] not in ["1", "2"]:
                board[y][x] = "."
    return (ss, board)

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
        return (False, ()) # There are no legal moves.
    for y in range(boardheight-1,-1,-1):
        if board[y][x] == ".":
            mark_board(steadystate, board, y, x, 1)
            return (True, (y,x))
    return (False, ())

def steadystateresponse(steadystate, board):
    alph = {}
    for x in range(boardwidth):
        for y in range(boardheight):
            letter = steadystate[y][x]
            if letter in miai:
                alph[letter] = alph.get(letter, 0) + 1
    for key in alph:
        if alph[key] > 2:
            return (False, ())
        if alph[key] == 1:
            for x in range(boardwidth):
                for y in range(boardheight):
                    if steadystate[y][x] == key:
                        if y!=boardheight-1 and board[y+1][x]=='.':
                            return (False, ())
                        mark_board(steadystate, board, y, x, 2)
                        return (True, (y,x))
            return (False, ())

    priorities = ["x"]*boardwidth
    for x in range(boardwidth):
        for y in range(boardheight-1, -1, -1):
            ss = steadystate[y][x]
            if ss != "1" and ss != "2":
                priorities[x] = ss
                # Claimeven
                if ss == ' ' and y%2==0:
                    mark_board(steadystate, board, y, x, 2)
                    return (True, (y,x))
                break


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
        return (False, ())
    mark_board(steadystate, board, y, x, 2)
    return (True, (y,x))

def check_winner(board, player, last_move):
    y, x = last_move
    #check horizontal spaces
    for i in range(max(0, x-3), min(x+1, boardwidth-3)):
        if board[y][i] == player and board[y][i+1] == player and board[y][i+2] == player and board[y][i+3] == player:
            return True

    #check vertical spaces
    if y+3 < boardheight:
        if board[y+1][x] == player and board[y+2][x] == player and board[y+3][x] == player:
            return True

    #check / diagonal spaces
    for i in range(max(0, x-3), min(x+1, boardwidth-3)):
        j = y - i + x
        if j < 3 or j >= boardheight:
            continue
        if board[j][i] == player and board[j-1][i+1] == player and board[j-2][i+2] == player and board[j-3][i+3] == player:
            return True

    # check \ diagonal spaces
    for i in range(max(0, x-3), min(x+1, boardwidth-3)):
        j = y - x + i
        if j < 0 or j > boardheight-4:
            continue
        if board[j][i] == player and board[j+1][i+1] == player and board[j+2][i+2] == player and board[j+3][i+3] == player:
            return True

    return False

def reproduce(steadystateslist, ssindex):
    whichoverwrite = random.randint(0,len(steadystateslist)-1)
    while whichoverwrite == ssindex:
        whichoverwrite = random.randint(0,len(steadystateslist)-1)
    r = random.random()
    if r<0.4:
        if r < 0.2:
            steadystateslist[whichoverwrite] = copy.deepcopy(steadystateslist[ssindex])
        else:
            y = random.randint(0, boardheight-1)
            x = random.randint(0, boardwidth-1)
            if steadystateslist[whichoverwrite][y][x] not in ['1','2']:
                steadystateslist[whichoverwrite][y][x] = random.choice(priority_list + miai + [' '])

def play_one_game(steadystate_original):
    (steadystate, board) = generate_board(steadystate_original)
    while True:
        #pprint(steadystate)
        (legal, coords) = play(steadystate, board)
        if not legal:
            return -1
        if check_winner(board, "1", coords):
            return -1
        (legal, coords) = steadystateresponse(steadystate, board)
        if not legal:
            return -1
        if check_winner(board, "2", coords):
            return 1















import unittest
class TestCheckWinner(unittest.TestCase):
    def test_horizontal_win(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        for x in range(boardwidth):
            for y in range(boardheight):
                self.assertTrue(check_winner(board, 1, (y,x)) == ((3 == y) and (x>=3)))

    def test_vertical_win(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 'x', 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ]
        for x in range(boardwidth):
            for y in range(boardheight):
                self.assertTrue(check_winner(board, 1, (y,x)) == ((y,x)==(2,3)))

    def test_diagonal_win(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0]
        ]
        for x in range(boardwidth):
            for y in range(boardheight):
                self.assertTrue(check_winner(board, 1, (y,x)) == ((x==y) and y>=2))

    def test_antidiagonal_win(self):
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0]
        ]
        for x in range(boardwidth):
            for y in range(boardheight):
                self.assertTrue(check_winner(board, 1, (y,x)) == (y>=2 and y+x==6))

    def test_known_steady_states(self):
        for steadystate in known_steadystates:
            pprint(steadystate)
            for i in range(100):
                assert(play_one_game(steadystate) == 1)

import sys

# Load and run the tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestCheckWinner)
result = unittest.TextTestRunner(verbosity=2).run(suite)

# Exit with an error code if any tests failed or had an error
if len(result.failures) > 0 or len(result.errors) > 0:
    sys.exit(1)

















generation = [copy.deepcopy(unproven[0]) for _ in range(100)]
while True:
    active = random.randint(0,len(generation)-1)
    wins = 0
    while True:
        if play_one_game(generation[active]) >= 0:
            wins+=1
            if wins % 1000 == 0:
                print(f"SteadyState wins! {wins}")
                pprint(generation[active])
            if wins == 100000:
                exit()
            reproduce(generation, active)
        else:
            print(wins)
            break
