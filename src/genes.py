import numpy as np


weights_1 = np.ones((12,5))
weights_2 = np.ones((5,2))
#worry about biases

#Do I  crossover for one or many weights (sets of chromosomes)?


pool = ['robot_1','robot_2', 'robot_3','robot_4'] #either contains objects of robots, or pointers to different list
#let's say already nown

def select_mating_pool(self):
    pass



#the crossover function is called within another function, where the parents are already selected (for that specific new gene

#assumes correlation in neural network between columns, switches columns
def crossover(self,a,b):
	
	#where a,b are parent 1 and parent 2 for this gene
	
	weights_A1 = a.weights1
	weights_B1 = b.weights1
	
	weights_A2 = a.weights2
	weights_B2 = b.weights2
	
	weights_C1 = np.zeros
	weights_C2 = np.zeros
	
	
	#taking alternating columns from each..
	weights_C1[0] = weights_A1[0]
	weights_C1[1] = weights_B1[1]
	weights_C1[2] = weights_A1[2]
	weights_C1[3] = weights_B1[3]
	# ... up until twelve?
	
	weights_C2 [0] = weights_A2[0]
	weights_C2 [1] = weights_A2[2]
	# ...up intil 5
	
	return weigths_C1, weights_C2
	

#no correlation, just switching, selection of gene is random, and number from each parent is random
def crossover2(self):
	
	weights_A1 = a.weights1
	weights_B1 = b.weights1
	
	weights_A2 = a.weights2
	weights_B2 = b.weights2
	
	weights_C1 = np.zeros
	weights_C2 = np.zeros
	
	for i in range(0, weights_C1[0].length):
		for j in range(0, weights_C1.length):
			
			random_choice = np.randit #
			if random_choice > 0.5:
				weights_C1[i][j] = weights_A1[i][j]
			if random_choice < 0.5:
				weights_C1[i][j] = weights_B1[i][j]
				
			....
			
	#also: choose randomly x spaces --> generate vector random positions 
	vector1 = [random.randint(1,weights_C1[0].length) for _ in range(number_genes/2)] ##
	vector2 = [random.randint(1,weights_C1.length) for _ in range(number_genes/2)]
	
	#This algorightm might lead to repetition
	
	for i in range(0, number_genes/2)
		a = vector1[i]
		b = vector2[i]
		weights_C1[a][b] = weights_A1[a][b]
		
		changed_matrix[a][b] = 1
		
	#keep matrix with count of genes changed
	#go throught it, if number is zero, use that to substitute with genes from other parent
	
	return weigths_C1, weights_C2
	

#no correlation, half of the weights come from each parent..
def crossover3(self):
	
	weights_A1 = a.weights1
	weights_B1 = b.weights1
	
	weights_A2 = a.weights2
	weights_B2 = b.weights2
	
	weights_C1 = np.zeros
	weights_C2 = np.zeros
	

	#also: choose randomly x spaces --> generate vector random positions 
	vector1 = [random.randint(1,weights_C1[0].length) for _ in range(number_genes/2)] ##
	vector2 = [random.randint(1,weights_C1.length) for _ in range(number_genes/2)]
	
	#This algorightm might lead to repetition
	
	for i in range(0, number_genes/2)
		a = vector1[i]
		b = vector2[i]
		weights_C1[a][b] = weights_A1[a][b]
		
		changed_matrix[a][b] = 1
		
	#keep matrix with count of genes changed
	#go throught it, if number is zero, use that to substitute with genes from other parent
	
	return weigths_C1, weights_C2




#
def mutation(self):
    pass



for i in range(0,list_robots_selected.length/2): #other option: while robots list not emoty
	
	a = 3 #pool[np.randint%%]
	b = 4 #pool[np.randint%%]
	
	crossover(a,b)
	
for (list children):
	#mutate
	pass
	
#average vs hereditary..
