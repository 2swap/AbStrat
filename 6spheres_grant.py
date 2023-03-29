import random
import copy

amount = 6
delta = .000001
learning_rate = 100
features = 'xyzr'

circles=[{'x':0, 'y':0, 'z':0, 'r':3}]
circles.append({'x':1, 'y':0, 'z':0, 'r':1})
circles.append({'x':-1.1, 'y':0, 'z':0, 'r':.5})
circles.append({'x':0, 'y':1, 'z':0, 'r':1})
circles.append({'x':0, 'y':-.5, 'z':.866, 'r':1})
circles.append({'x':0, 'y':-.5, 'z':-.867, 'r':1})
#for i in range(amount-1):
#	circles.append({'x':random.uniform(-5, 5), 'y':random.uniform(-5, 5), 'z':random.uniform(-5, 5), 'r':random.uniform(.1,.2)})

def circle_dist(c1, c2):
	center_dist = ((c1['x']-c2['x'])**2+(c1['y']-c2['y'])**2+(c1['z']-c2['z'])**2)**.5
	dists = [center_dist, c1['r'], c2['r']]
	dists.sort()
	return ((dists[2]-dists[1]-dists[0])/dists[0])**2

def all_circles_dists(circles):
	dist = 0
	for i in range(amount):
		for j in range(i):
			dist += circle_dist(circles[i], circles[j])
	return dist

mse = copy.deepcopy(circles)
curr_mse = 1000
while curr_mse > .001:
	curr_mse = all_circles_dists(circles)
	print(curr_mse)
	for c in range(amount):
		for f in features:
			circles[c][f] += delta
			mse[c][f] = all_circles_dists(circles)-curr_mse
			circles[c][f] -= delta
	for c in range(amount):
		for f in features:
			circles[c][f] -= learning_rate*mse[c][f]
	bigr = circles[0]['r']
	if bigr > 100 or bigr < .1:
		print("oh no!")
		print(bigr)
print(circles)
