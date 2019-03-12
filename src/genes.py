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


def crossover2(self, robots_selected):
	# assuming this list is always even...

	# takes all parents in
	# should return children

	# random numbe between 0 and 1 * len list selected
	# move this into random list... (funtion for randomly sort a list)?
	# remove from that list

	robtos_random = []

	# if length list is not constant, create a new variable with original length list
	for i in range(0, robots_selected):  # does length stay constant, even if loop reducing...
		a = np.random  # rundom number 0 and 1
		index = a * robots_selected.length  # this is NEW length
		robots_random.append(robots_selected[i])  # check..
		del robots_selected[i]  # check #so that this robot is chosen only once

	offspring_list = []

	# now, select in pairs and apply misture
	for i in range(0, robots_random.length / 2):
		k = 2 * i
		offspring = mixture(robots_random(k), robots_random(k + 1))  ##Here is where they mix
		offspring_list.append(offspring)  # check

	return offspring_list


def mixture2(parent1, parent2):  # way of crossing genes..

	weights_A1 = a.weights1
	weights_B1 = b.weights1

	weights_A2 = a.weights2
	weights_B2 = b.weights2

	weights_C1 = np.zeros  # create new instance robot?
	weights_C2 = np.zeros

	changed_matrix1 = np.zeros
	changed_matrix2 = np.zeros

	# also: choose randomly x spaces --> generate vector random positions
	vectorx1 = [random.randint(1, weights_C1[0].length) for _ in range(number_genes / 2)]  ##assume even?
	vectory1 = [random.randint(1, weights_C1.length) for _ in range(number_genes / 2)]

	vectorx2 = [random.randint(1, weights_C2[0].length) for _ in range(number_genes / 2)]  ##assume even?
	vectory2 = [random.randint(1, weights_C2.length) for _ in range(number_genes / 2)]

	# this might repeat some...

	for i in range(0, number_genes / 2):  # this range needs to corrected I beleive..
		a = vectorx1[i]
		b = vectory1[i]
		weights_C1[a][b] = weights_A1[a][b]
		changed_matrix1[a][b] = 1

	for i in range(0, changed_matrix1.length):
		for j in range(0, changed_matrix1.length):
			if changed_matrix1[i][j] == 0:  # has not been changed, mean this is for the other parent to fill in
				weights_C1[i][j] = weights_B1[i][j]

	# weights2 ##NEEDS TO BE ADJUSTED
	for i in range(0, number_genes / 2):
		a = vectorx2[i]
		b = vectory2[i]
		weights_C2[a][b] = weights_A2[a][b]
		changed_matrix2[a][b] = 1

	for i in range(0, changed_matrix2.length):
		for j in range(0, changed_matrix2.length):
			if changed_matrix2[i][j] == 0:  # has not been changed, mean this is for the other parent to fill in
				weights_C2[i][j] = weights_B2[i][j]

	return weight_C1, weights_C2


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
