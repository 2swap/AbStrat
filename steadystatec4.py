from pprint import pprint
import copy, math
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
    list("  111| "),
    list("  222| "),
    list("  112| "),
    list("  221| "),
    list("  112| "),
    list("  221-2")
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
    list("   +   "),
    list("   -   "),
    list("   2   "),
    list("  11 =-"),
    list("  21 2+")
    ],
    [
    list("- -=  -"),
    list("- -2  #"),
    list("-121  #"),
    list("-112+-@"),
    list("12221-@"),
    list("22121--")
    ],
    [
    list("   #   "),
    list("   2  ="),
    list(" 211  -"),
    list(" 112+-+"),
    list("12221--"),
    list("22121=#")
    ],
    [
    list("   -   "),
    list("   +   "),
    list("   =   "),
    list("   2   "),
    list("-=211  "),
    list("=2112  "),
    ],
    [
    list("   -   "),
    list("   +   "),
    list("   -   "),
    list("   2   "),
    list("-=21# #"),
    list("=2112 1"),
    ],
    [
    list(" #-#|@="),
    list(" 1=2|2="),
    list(" 2-1|2="),
    list(" 1=2|1="),
    list(" 2-1|2="),
    list(" 1=2@1="),
    ],
    [
    list(" |=1   "),
    list(" ||2   "),
    list("+| 1-  "),
    list("+|22|  "),
    list("+|21-  "),
    list("+1122  "),
    ],
    [
    list("  + | |"),
    list("  1 | |"),
    list("  2 |2|"),
    list("  1 |1|"),
    list("  22 2|"),
    list("  12=1|"),
    ],
    [
    list("  +  =|"),
    list("  1||||"),
    list("  22 2|"),
    list("  12-1|"),
    list("  21 2|"),
    list("  12-1#"),
    ],
    [
    list("|  =  +"),
    list("|  2  |"),
    list("|  1+ ="),
    list("|-@211="),
    list("|=12221"),
    list("--12122")
    ],
    [
    list("  | x  "),
    list("  | x  "),
    list("  |2x1 "),
    list("  |1=1 "),
    list("  |2=22"),
    list("  12=21"),
    ],
    [
    list("  |+x  "),
    list("  |1x  "),
    list("  |2x  "),
    list("  |1=1 "),
    list("  |2 22"),
    list("  12=21"),
    ],
    [
    list(" =+1+= "),
    list(" |122||"),
    list("  2112="),
    list("-|1221|"),
    list("=22121="),
    list("121221-"),
    ],
    [
    list("- +2+2+"),
    list("- -2+1-"),
    list("- 21=2+"),
    list("+-12+1|"),
    list("- 21+2-"),
    list("1-12=1+")
    ],
    [
    list("   |@  "),
    list("   |2  "),
    list("  2|2  "),
    list("  1|1  "),
    list("  1|21@"),
    list("  12122")
    ],
    [
    list("@ 21+@|"),
    list("2 12+2|"),
    list("1 11+2|"),
    list("2 12+11"),
    list("1221222"),
    list("2112121")
    ],
    [
    list(" =+1+=|"),
    list(" #122||"),
    list(" 22112|"),
    list(" 11221|"),
    list("-12121|"),
    list("221221+")
    ],
    [
    list(" 12    "),
    list(" 21    "),
    list(" 12 +  "),
    list(" 21 +  "),
    list(" 12   -"),
    list(" 12 @ @"),
    ],
]

unproven=[
    [
    list("   1   "),
    list("   2   "),
    list("   1   "),
    list("   2   "),
    list("  -1 @+"),
    list("  21 2@")
    ],
    [
    list("--21-- "),
    list("++22++ "),
    list("--21-- "),
    list("  12   "),
    list("  211  "),
    list("  122  "),
    ],
]
num_coevolution = 100
last_defeats=[""]*num_coevolution

boardheight = 6
boardwidth = 7
priority_list = ["+", "=", "-"]
miai = ['@','#']
claims = [' ', '|']

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
    print("this shouldnt happen")
    exit()

def play_with_coevolution(steadystate, board, coevolution, moveno):
    x = -1
    indices = [i for i, x in enumerate(board[0]) if x == '.'] # get indices of all legal moves
    if moveno < len(coevolution) and int(coevolution[moveno]) in indices:
        x = int(coevolution[moveno])
    elif indices: # if there is a legal move
        x = random.choice(indices) # choose a random index from the list of indices
    else:
        return (False, ()) # There are no legal moves.
    for y in range(boardheight-1,-1,-1):
        if board[y][x] == ".":
            mark_board(steadystate, board, y, x, 1)
            return (True, (y,x))
    print("this shouldnt happen")
    exit()

def steadystateresponse(steadystate, board):
    # First Priority: Obey Miai
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
                        # Forfeit if there is an unpaired unplayable miai
                        if y!=boardheight-1 and board[y+1][x]=='.':
                            return (False, ())
                        mark_board(steadystate, board, y, x, 2)
                        return (True, (y,x))
            return (False, ())

    # Second Priority: Claimeven and Claimodd
    priorities = ["x"]*boardwidth
    for x in range(boardwidth):
        for y in range(boardheight-1, -1, -1):
            ss = steadystate[y][x]
            if ss != "1" and ss != "2":
                # Claimeven
                if ss == ' ' and y%2==0:
                    mark_board(steadystate, board, y, x, 2)
                    return (True, (y,x))
                # Claimodd
                if ss == '|' and y%2==1:
                    mark_board(steadystate, board, y, x, 2)
                    return (True, (y,x))
                priorities[x] = ss
                break

    # Third Priority: Follow Priority
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
    r = random.random()
    steadystateslist[whichoverwrite] = copy.deepcopy(steadystateslist[ssindex])
    y = random.randint(0, boardheight-1)
    x = random.randint(0, boardwidth-1)
    if steadystateslist[whichoverwrite][y][x] not in ['1','2']:
        steadystateslist[whichoverwrite][y][x] = random.choice(priority_list + miai + claims + [' ', ' '])

debug = False
def play_one_game(steadystate_original):
    (steadystate, board) = generate_board(steadystate_original)
    defeat_pattern = ""
    if debug:
        print('\n\n\n\n\n\n\n')
    while True:
        if debug:
            print('\n')
        (legal, coords) = play(steadystate, board)
        if debug:
            pprint(board)
        if not legal:
            break
        defeat_pattern += str(coords[1])
        if check_winner(board, "1", coords):
            if debug:
                exit()
            break
        (legal, coords) = steadystateresponse(steadystate, board)
        if debug:
            pprint(board)
        if not legal:
            break
        if check_winner(board, "2", coords):
            return 1
    last_defeats[int(random.random()*num_coevolution)] = defeat_pattern
    return -1

def play_one_game_with_coevolution(steadystate_original, coevolution):
    (steadystate, board) = generate_board(steadystate_original)
    defeat_pattern = ""
    moveno = 0
    while True:
        (legal, coords) = play_with_coevolution(steadystate, board, coevolution, moveno)
        moveno+=1
        if not legal:
            break
        defeat_pattern += str(coords[1])
        if check_winner(board, "1", coords):
            break
        (legal, coords) = steadystateresponse(steadystate, board)
        if not legal:
            break
        if check_winner(board, "2", coords):
            return 1
    last_defeats[int(random.random()*num_coevolution)] = defeat_pattern
    return -1















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
        """
        [['.', '.', '.', '1', '.', '.', '.'],
         ['.', '.', '.', '1', '.', '.', '.'],
         ['2', '.', '1', '2', '.', '2', '1'],
         ['1', '.', '2', '1', '.', '1', '1'],
         ['2', '.', '2', '2', '.', '2', '2'],
         ['1', '.', '1', '2', '.', '2', '1']]
        [['.', '.', '.', '1', '.', '.', '.'],
         ['.', '.', '2', '1', '.', '.', '.'],
         ['2', '.', '1', '2', '.', '2', '1'],
         ['1', '.', '2', '1', '.', '1', '1'],
         ['2', '.', '2', '2', '.', '2', '2'],
         ['1', '.', '1', '2', '.', '2', '1']]


        [['.', '.', '.', '1', '.', '.', '.'],
         ['.', '.', '2', '1', '.', '.', '1'],
         ['2', '.', '1', '2', '.', '2', '1'],
         ['1', '.', '2', '1', '.', '1', '1'],
         ['2', '.', '2', '2', '.', '2', '2'],
         ['1', '.', '1', '2', '.', '2', '1']]
        [['.', '.', '2', '1', '.', '.', '.'],
         ['.', '.', '2', '1', '.', '.', '1'],
         ['2', '.', '1', '2', '.', '2', '1'],
         ['1', '.', '2', '1', '.', '1', '1'],
         ['2', '.', '2', '2', '.', '2', '2'],
         ['1', '.', '1', '2', '.', '2', '1']]


        [['.', '.', '2', '1', '.', '.', '1'],
         ['.', '.', '2', '1', '.', '.', '1'],
         ['2', '.', '1', '2', '.', '2', '1'],
         ['1', '.', '2', '1', '.', '1', '1'],
         ['2', '.', '2', '2', '.', '2', '2'],
         ['1', '.', '1', '2', '.', '2', '1']]
        """

    def test_known_steady_states(self):
        for steadystate in known_steadystates:
            pprint(steadystate)
            for i in range(200):
                assert(play_one_game(steadystate) == 1)

import sys

# Load and run the tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestCheckWinner)
result = unittest.TextTestRunner(verbosity=2).run(suite)
# Exit with an error code if any tests failed or had an error
if len(result.failures) > 0 or len(result.errors) > 0:
    sys.exit(1)


















currbest = 1
generation = [copy.deepcopy(unproven[0]) for _ in range(1000)]
for i in range(len(generation)):
    y = random.randint(0, boardheight-1)
    x = random.randint(0, boardwidth-1)
    if generation[i][y][x] not in ['1','2']:
        generation[i][y][x] = random.choice(priority_list + miai + claims + [' ', ' '])


while True:
    active = random.randint(0,len(generation)-1)
    wins = 0
    coe = 0
    while True:
        play_one = 0
        if random.random() < 0.98 or coe >= num_coevolution:
            play_one = play_one_game(generation[active])
        else:
            play_one = play_one_game_with_coevolution(generation[active], last_defeats[coe])
            coe += 1
        if play_one >= 0:
            wins+=1
            if wins % 500 == 99:
                print(f"SteadyState wins! {wins}")
                pprint(generation[active])
            if wins == 100000:
                exit()
        else:
            for i in range(int(wins/2)):
                reproduce(generation, active)
            if wins > currbest:
                currbest = wins
                print(wins)
            break
