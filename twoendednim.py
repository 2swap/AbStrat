from pprint import pprint

def move(state, cut):
    moved = state[cut:]
    return moved[-1::-1]

memo = {
    "wl": {"win": ["win"], "tie": [],      "lose": []      },
    "lw": {"win": [],      "tie": [],      "lose": ["lose"]},
    "ww": {"win": [],      "tie": ["tie"], "lose": []      },
    "ll": {"win": [],      "tie": ["tie"], "lose": []      },
}
def solve(state):
    if state not in memo:
        memo[state] = {"win": [], "tie": [], "lose": []}
        if state.isnumeric():
            if len(state) == 2:
                if state[0]>state[1]:
                    memo[state] = {"win": ["win"], "tie": [], "lose": []}
                elif state[0] == state[1]:
                    memo[state] = {"win": [], "tie": ["tie"], "lose": []}
                else:
                    memo[state] = {"win": [], "tie": [], "lose": ["lose"]}
        else:
            assert(len(state) > 2)
        for cut in [1,2,3,4]:
            if cut + 2 > len(state):
                continue
            if len(solve(move(state, cut))["win"]) > 0:
                memo[state]["lose"].append(cut)
            elif len(solve(move(state, cut))["tie"]) > 0:
                memo[state]["tie"].append(cut)
            else:
                memo[state]["win"].append(cut)
    return memo[state]

# Unit Tests
assert(move("wlwl" , 1) == "lwl" )
assert(move("wlwlw", 1) == "wlwl")
assert(move("wlwlw", 2) == "wlw" )
assert(move("wlwlw", 3) == "wl"  )
assert(solve("wlw"     ) == {"win": []    , "tie": []          , "lose": [1]         })
assert(solve("wlwlw"   ) == {"win": [2]   , "tie": []          , "lose": [1, 3]      })
assert(solve("lwlw"    ) == {"win": [1]   , "tie": []          , "lose": [2]         })
assert(solve("lwlwlwlw") == {"win": []    , "tie": []          , "lose": [1, 2, 3, 4]})
assert(solve("lwlwwlw" ) == {"win": [4]   , "tie": [3]         , "lose": [1, 2]      })
assert(solve("lwllllw" ) == {"win": []    , "tie": [1, 2, 3, 4], "lose": []          })
assert(solve("lwlllw"  ) == {"win": []    , "tie": [1, 2, 3]   , "lose": [4]         })
assert(solve("43215"   ) == {"win": [1, 2], "tie": []          , "lose": [3]         })

def blurb(state):
    solve(state)
    print(f"{state}: {memo[state]}")

pos = "017412364518721734650"
pos = move(pos, 4)
pos = move(pos, 3)

pos = move(pos, 4)
pos = move(pos, 4)
print(len(pos))

blurb(pos)
#pprint(memo)

#blurb("wlwlwlwwwlwlwlllwlwlllwlwwwllwllwlllwlllwwwwwwlllllwlwlwllwlwlllwwwwllwlllwlwlwwwllwllwlwllwllwllwlwllwlwlwlllwwwwllwlllwlwlwwwllwllwlwllwllwllwlwllwwllwlwwlwlwwlwllwlwlwllwlwlllwwwwlwllwllwllwwlwlwllwllwwwlllwlwlllwllwlwlwwwll")
#blurb(move(move("wllwlwllwlwwllwlwlwlwlwlwwllwlwllwllw", 4), 4))