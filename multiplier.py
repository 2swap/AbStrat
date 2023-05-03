def max_int_in_str(s):
    return max(str_to_list(s))

def find_unused(board):
    unused = []
    for i in range(1,10):
        if str(i) not in board:
            unused.append(str(i))
    return unused

def sort_rows(board):
    rows = [f"{board[0]}{board[1]}{board[2]}", f"{board[3]}{board[4]}{board[5]}", f"{board[6]}{board[7]}{board[8]}"]
    if max_int_in_str(rows[1]) > max_int_in_str(rows[0]):
        temp = rows[0]
        rows[0] = rows[1]
        rows[1] = temp
    if max_int_in_str(rows[2]) > max_int_in_str(rows[1]):
        temp = rows[1]
        rows[1] = rows[2]
        rows[2] = temp
    if max_int_in_str(rows[1]) > max_int_in_str(rows[0]):
        temp = rows[0]
        rows[0] = rows[1]
        rows[1] = temp
    return rows[0]+rows[1]+rows[2]

def sort_columns(board):
    return transpose(sort_rows(transpose(board)))

def collapse(board):
    return sort_rows(sort_columns(board))

def move(board, y, x, num):
    assert(num not in board)
    i = x+y*3
    assert(board[i] == '0')
    board = board[0:i]+num+board[i+1:]
    return transpose(collapse(board))

def str_to_list(board_str):
    board=[]
    for c in board_str:
        board.append(int(c))
    return board

def score_for_horizontal(board_str):
    board = str_to_list(board_str)
    topmult = board[0]*board[1]*board[2]
    midmult = board[3]*board[4]*board[5]
    lowmult = board[6]*board[7]*board[8]
    horizontal_score = topmult+midmult+lowmult
    
    lftmult = board[0]*board[3]*board[6]
    ctrmult = board[1]*board[4]*board[7]
    rgtmult = board[2]*board[5]*board[8]
    vertical_score = lftmult+ctrmult+rgtmult

    return horizontal_score - vertical_score

def transpose(board):
    return f"{board[0]}{board[3]}{board[6]}{board[1]}{board[4]}{board[7]}{board[2]}{board[5]}{board[8]}"

def print_board(board_str):
    board = str_to_list(board_str)
    topmult = board[0]*board[1]*board[2]
    midmult = board[3]*board[4]*board[5]
    lowmult = board[6]*board[7]*board[8]
    print(f"{board[0]}  {board[1]}  {board[2]}   |   {topmult}")
    print(f"{board[3]}  {board[4]}  {board[5]}   |   {midmult}   ->   {topmult + midmult + lowmult}")
    print(f"{board[6]}  {board[7]}  {board[8]}   |   {lowmult}")
    lftmult = board[0]*board[3]*board[6]
    ctrmult = board[1]*board[4]*board[7]
    rgtmult = board[2]*board[5]*board[8]
    print(f"{lftmult}  {midmult}  {rgtmult}")
    print(f"   {lftmult+ctrmult+rgtmult}")

memo = {}
def solve(board):
    collapse(board)
    if board not in memo:
        # leaf node
        if "0" not in board:
            memo[board] = (score_for_horizontal(board), (-1, -1, -1))

        # recursive call
        else:
            memo[board] = (-10000, (-1,-1,-1))
            unused = find_unused(board)
            for y in [0,1,2]:
                for x in [0,1,2]:
                    if board[x+y*3] == '0':
                        for num in unused:
                            test_score = -solve(move(board, y, x, num))
                            if test_score > memo[board][0]:
                                memo[board] = (test_score, (y, x, num))
    return memo[board][0]

def blurb(board):
    unused = find_unused(board)
    for y in [0,1,2]:
        for x in [0,1,2]:
            if board[x+y*3] == '0':
                print("(", end="")
                for num in unused:
                    print(f"{num}={solve(move(board, y, x, num))},", end="")
                print(") ", end="")
            else:
                print("xxx ", end="")
        print("\n")







# Unit Tests
assert(score_for_horizontal("123456789") == 360)
assert(score_for_horizontal("123456798") == 368)
assert(max_int_in_str("123456789") == 9)
assert(transpose("123456789") == "147258369")
assert(sort_rows("123456789") == "789456123")
assert(sort_columns("123456789") == "321654987")
assert(collapse("123456789") == "987654321")
assert(move("123400000", 2, 1, "9") == transpose("900040213"))
assert(find_unused("123400000") == ["5","6","7","8","9"])
print(solve(transpose("123456000")))
print(solve(("123456700")))
print(solve(("123456070")))
print(solve(("123456007")))
print(solve(("123456800")))
print(solve(("123456080")))
print(solve(("123456008")))
print(solve(("123456900")))
print(solve(("123456090")))
print(solve(("123456009")))
assert(solve("123456700") == 368)
assert(solve("147250360") == -360)

brd = "983752416"
print_board(brd)
solve(brd)
blurb(brd)

print(f"memo length: {len(memo)}")
