from pprint import pprint
from math import log, floor

def is_decreasing(arr):
    for i in range(len(arr)-1):
        if arr[i] < arr[i+1]:
            return False
    return True

# number of partitions of n objects such that no partition has fewer than b objects
memo = {}
def f(n,b):
    if (n,b) in memo:
        return memo[(n,b)]
    cnt = 1
    for i in range(floor((n+1)/2), n-b+1):
        first, last = i, n-i
        cnt += f(first, last)
    memo[(n,b)] = cnt
    return cnt


def get_children(partition):
    children = []
    children.append(partition)
    first = partition[0]
    for i in range(first-1):
        child = partition.copy()
        child.pop(0)
        child.insert(0,i+1)
        child.insert(0,first-(i+1))
        if is_decreasing(child):
            children.extend(get_children(child))
    return children

def get_diff(arr):
    diff = []
    for i in range(len(arr)-1):
        diff.append(arr[i+1]-arr[i])
    return diff

pos = []
pos2 = []
for i in range(100):
    #x = len(get_children(start))
    #pos.append(x)
    pos2.append(f(i, 1))

pprint(pos)
pprint(memo)
pprint(pos2)
#pprint(get_diff(get_diff(pos)))
#pprint(get_diff(get_diff(get_diff(pos))))
