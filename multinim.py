from copy import deepcopy
from pprint import pprint

memo = {(0,0): []}
# find winning moves
def solve(state):
    if state not in memo:
        memo[state] = []
        for i in range(len(state)):
            for newnum in range(0, state[i]):
                new_state = list(deepcopy(state))
                new_state[i] = newnum
                new_state = tuple(new_state)
                if len(solve(new_state))==0:
                    memo[state].append(new_state)
    return memo[state]

# Unit Tests
assert(solve((1,0)) == [(0,0)])
assert(solve((1,1)) == [])
assert(solve((2,0)) == [(0,0)])
assert(solve((2,1)) == [(1,1)])
assert(solve((2,2)) == [])

def blurb(state):
    solve(state)
    print(f"{state}: {memo[state]}")

w = 4
g = {}
for a in range(w):
    for z in range(w):
        for y in range(w):
            for x in range(w):
                s = len(solve((a,z,y,x)))
                print(s, end="")
                if a+x+y+z not in g:
                    g[a+x+y+z] = []
                if s not in g[a+x+y+z]:
                    g[a+x+y+z].append(s)
            print()
        print()
    print()
