import numpy as np


weights_1 = np.ones((12,5))
weights_2 = np.ones((5,2))
#worry about biases

#Do I  crossover for one or many weights (sets of chromosomes)?


pool = ['robot_1','robot_2', 'robot_3'] #either contains objects of robots, or pointers to different list

def select_mating_pool(self):
    pass

def crossover(self):
	
	
	weights_A1 = a.weights1
	weights_B1 = b.weights1
	
	weights_A2 = a.weights2
	weights_B2 = b.weights2
	
	weights_C1 = np.zeros
	weights_C2 = np.zeros
	
	weights_C1[0] = weights_A1[0]
	weights_C1[1] = weights_B1[1]
	weights_C1[2] = weights_A1[2]
	weights_C1[3] = weights_B1[3]
	... up until twelve?
	
	weights_C2 [0] = weights_A2[0]
	weights_C2 [1] = weights_A2[2]
	...up intil 5
	
    return weigths_C1, weights_C2

def mutation(self):
    pass



for (list_robots_selected.length/2): #while robots list not emoty
	
	a = pool[np.randint%%]
	b = pool[np.randint%%]
	
	crossover(a,b)
	
for (list children):
	#mutate
	pass
	
