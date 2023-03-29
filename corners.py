import random

def mirror(x):
	dupeOp(x)
	dupeOp(x+5)

def dupeOp(x):
	swap(x, x+1)
	swap(x+2, x+3)

def swap(x, y):
	x%=10
	y%=10
	temp = perm[x]
	perm[x] = perm[y]
	perm[y] = temp

#perm = [10, 1, 3, 5, 8, 0, 4, 7, 9, 11, 2, 6]
#mirror(3)
#print(perm)

for attempt in range(1000000):
	perm = [0, 1, 4, 2, 3, 5, 6, 9, 7, 8]
	movelist = []
	i = 0
	while True:
		val = random.choice(range(0, 5))
		movelist.append(val)
		mirror(val)
		i+=1
		if perm == [0,1,2,3,4,5,6,7,8,9]:
			print(str(i) + " " + str(movelist))
			break
		if i>1:
			break


