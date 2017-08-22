import gameboard
import filereader
import sys
import variable
import constraint
import constraintnetwork



# def partition(array, begin, end):
#     pivot = begin
#     for i in range(begin+1, end+1):
#         if len(array[i][1]) <= len(array[begin][1]):
#             pivot += 1
#             array[i], array[pivot] = array[pivot], array[i]
#     array[pivot], array[begin] = array[begin], array[pivot]
#     return pivot

# def quicksort(array, begin=0, end=None):
#     if end is None:
#         end = len(array) - 1
#     def _quicksort(array, begin, end):
#         if begin >= end:
#             return
#         pivot = partition(array, begin, end)
#         _quicksort(array, begin, pivot-1)
#         _quicksort(array, pivot+1, end)
#     return _quicksort(array, begin, end)

# def partition2(array, begin, end):
#     pivot = begin
#     for i in range(begin+1, end+1):
#         if array[i][1] <= array[begin][1]:
#             pivot += 1
#             array[i], array[pivot] = array[pivot], array[i]
#     array[pivot], array[begin] = array[begin], array[pivot]
#     return pivot

# def quicksort2(array, begin=0, end=None):
#     if end is None:
#         end = len(array) - 1
#     def _quicksort(array, begin, end):
#         if begin >= end:
#             return
#         pivot = partition2(array, begin, end)
#         _quicksort(array, begin, pivot-1)
#         _quicksort(array, pivot+1, end)
#     return _quicksort(array, begin, end)

# #### MRV ####

# def get_min(array):
#   mini = array[0]
#   for i in array:
#     if len(i[1]) < len(mini[1]):
#     	mini = i
#   return mini

# def MRV():
# 	sudokudata = filereader.SudokuFileReader(sys.argv[1])
# 	print(sudokudata)
# 	network = filereader.GameBoardToConstraintNetwork(sudokudata)
# 	templist = []
# 	for v in network.variables:
# 		if not v.isAssigned():
# 			templist.append((v, MRV_helper(network, v)))
# 	quicksort(templist)

# def MRV_helper(cn, v):
# 	outlist = {1, 2, 3, 4, 5, 6, 7, 8, 9} # initial set of domain values in temp list
# 	list_of_constraints = cn.getConstraintsContainingVariable(v)
# 	for c in list_of_constraints: # for each constraint for variable v
# 		# print(c) # print each constraint containting variable v
# 		for var in c.vars: # for each variable in the constraint
# 			if var.isAssigned(): # if the variable is assigned (has only one value)
# 				if var.domain.values[0] in outlist:
# 					outlist.remove(var.domain.values[0]) #remove the value in the domain from the temp list
# 	return list(outlist)



# def Degree():
# 	sudokudata = filereader.SudokuFileReader(sys.argv[1])
# 	print(sudokudata)	

# 	network = filereader.GameBoardToConstraintNetwork(sudokudata)
# 	templist = []
# 	for v in network.variables:
# 		if not v.isAssigned():
# 			templist.append((v, DegreeHelper(network, v)))
# 	quicksort(templist)
# 	templist.reverse()
# 	for i in templist:
# 		print((i[0].name, len(i[1])))

# def DegreeHelper(network, v):
# 	list_of_constraints = network.getConstraintsContainingVariable(v)
# 	outlist = set()
# 	for c in list_of_constraints:
# 		for var in c.vars:
# 			if not var.isAssigned():
# 				outlist.add(var)
# 	return list(outlist)




# def LCV():
# 	sudokudata = filereader.SudokuFileReader(sys.argv[1])
# 	print(sudokudata)	



# 	network = filereader.GameBoardToConstraintNetwork(sudokudata)
# 	v = network.variables[11]
# 	lcv_list = getLCV(network, v)
# 	quicksort2(lcv_list)
# 	print(lcv_list)


# def getLCV(network, v):
# 	lcv_list = []
# 	for i in range(0, self.gameboard.N):
# 		lcv_list.append([i+1, 0])
		
# 	list_of_constraints = network.getConstraintsContainingVariable(v)
# 	print(v)
# 	for i in network.getNeighborsOfVariable(v):
# 		print (i)
# 		if i.isAssigned():
# 			v.removeValueFromDomain(i.domain.values[0])
# 		print(i)


# 	for c in list_of_constraints:
# 		for var in c.vars:
# 			if var.isAssigned():
# 				lcv_list[var.domain.values[0] - 1][1] += 1

# 	return lcv_list


# def NKP():
# 	sudokudata = filereader.SudokuFileReader(sys.argv[1])
# 	print(sudokudata)	
# 	network = filereader.GameBoardToConstraintNetwork(sudokudata)
# 	blocks = getConstraintBlocks(network, sudokudata)
# 	rows = getConstraintRows(network, sudokudata)
# 	cols = getConstraintColumns(network, sudokudata)

# 	list_of_constraints = network.getConstraintsContainingVariable(network.variables[0])
# 	neighbor = network.getNeighborsOfVariable(network.variables[0])

# 	elim_set = set()
# 	for c in list_of_constraints:
# 		for v in c.vars:
# 			if not v.isAssigned():
# 				eliminateDomain(network, v)
# 				elim_set.add(v)

# 	for i in elim_set:
# 		print(i)
# 	print(len(elim_set))



# def getConstraintRows(network, gb):
# 	rows = set()
# 	for i in range(0, len(network.variables), gb.N):
# 		list_of_constraints = network.getConstraintsContainingVariable(network.variables[i])
# 		rows.add(list_of_constraints[0])
# 	return list(rows)

# def getConstraintColumns(network, gb):
# 	cols = set()
# 	for i in range(0, gb.N):
# 		list_of_constraints = network.getConstraintsContainingVariable(network.variables[i])
# 		cols.add(list_of_constraints[1])
# 	return list(cols)

# def getConstraintBlocks(network, gb):
# 	blocks = set()
# 	for i in range(0, len(network.variables), gb.q):
# 		list_of_constraints = network.getConstraintsContainingVariable(network.variables[i])
# 		blocks.add(list_of_constraints[2])
# 	return list(blocks)

# def eliminateDomain(network, v):
# 	neighbor = network.getNeighborsOfVariable(v)
# 	for n in neighbor:
# 		if n.isAssigned():
# 			if n.domain.values[0] in v.domain.values:
# 				v.removeValueFromDomain(n.domain.values[0])
# 	return v








# def getNakedConstraintsOfVariable(network, v):
#     	elim_set = set()
#     	for c in network.getConstraintsContainingVariable(v):
#     		for v in c.vars:
#     			if not v.isAssigned():
#     				eliminateDomainOfVariable(network, v)
#     				elim_set.add(v)
#     	return elim_set 
  
# def eliminateDomainOfVariable(network, v):
#     	neighbors = network.getNeighborsOfVariable(v)
#     	for n in neighbors:
#     		if n.isAssigned():
#     			if n.domain.values[0] in v.domain.values:
#     				v.removeValueFromDomain(n.domain.values[0])
#     	return v
def NKT(network):
	for v in network.variables:
		if not v.isAssigned():
			elim_set = reducedDomainConstraintSet(network, v)
			if v.size() == 3:
				print("\n~~ Elim set of {} ~~".format(v))
				for i in elim_set:
					# print("~~~~")
					tup = (v,)
					for l in i:
						# print(l)
						if not l.isAssigned() and l.size() < 4 and l != v and isSubset(v, l):
							tup += (l,)
							if len(tup) == 3:
								print("NAKER TRIPLE!")
								reduceWithNakedTriple(network, tup)



def isSubset(v, v2):
	if v.size() < v2.size():
		return False
	for val in v2.Values():
		if not val in v.Values():
			return False
	return True

def reducedDomainConstraintSet(network, v):
	cList = []
	for c in network.getConstraintsContainingVariable(v): # [0] = row [1] = col [2] = blck
		cSet = set()
		for var in c.vars:
			for n in network.getNeighborsOfVariable(var):
				if n.isAssigned():
					var.removeValueFromDomain(n.domain.values[0])
			cSet.add(var)
		cList.append(cSet)
	return cList

def reduceWithNakedTriple(network, nkt):
	union_set = set()
	for i in network.getNeighborsOfVariable(nkt[0]):
		if i in network.getNeighborsOfVariable(nkt[1]) and i in network.getNeighborsOfVariable(nkt[2]):
			union_set.add(i)
	for v in union_set:
		if v != nkt[0] and v != nkt[1] and v != nkt[2]:
			if nkt[0].domain.values[0] in v.domain.values:
				v.removeValueFromDomain(nkt[0].domain.values[0])
			if nkt[0].domain.values[1] in v.domain.values:
				v.removeValueFromDomain(nkt[0].domain.values[1])
			if nkt[0].domain.values[2] in v.domain.values:
				v.removeValueFromDomain(nkt[0].domain.values[2])



def NKP(network):

	for v in network.variables:
		if not v.isAssigned():
			for i in getNakedPairConstraintsOfVariable(network, v):
				if not i.isAssigned():
					if v.domain.size() == 2 and v != i and i.domain.size() == 2:
						if i.domain.values[0] == v.domain.values[0] and i.domain.values[1] == v.domain.values[1]:
							reduceDomainsWithNakedPair(network, (v, i))


	return True


def getNakedPairConstraintsOfVariable(network, v):
    	elim_set = set()
    	for c in network.getConstraintsContainingVariable(v):
    		for v in c.vars:
    			if not v.isAssigned():
    				removeAssignedNeighborsFromDomain(network, v)
    				elim_set.add(v)

    	return elim_set 


def reduceDomainsWithNakedPair(network, nkp): #nkp is a 2-tuple
	union_set = set()
	n1 = network.getNeighborsOfVariable(nkp[0])
	n2 = network.getNeighborsOfVariable(nkp[1])
	for v in n1:
		if v in n2:
			union_set.add(v)
			for v in union_set:
				if v != nkp[0] and v != nkp[1]:
					if nkp[0].domain.values[0] in v.domain.values:
						v.removeValueFromDomain(nkp[0].domain.values[0])
					if nkp[0].domain.values[1] in v.domain.values:
						v.removeValueFromDomain(nkp[0].domain.values[1])


def removeAssignedNeighborsFromDomain(network, v):
	n = network.getNeighborsOfVariable(v)
	for i in n:
		if i.isAssigned():
			if i.domain.values[0] in v.Values():
				v.removeValueFromDomain(i.domain.values[0])



def main():
	sudokudata = filereader.SudokuFileReader(sys.argv[1])
	print(sudokudata)	
	network = filereader.GameBoardToConstraintNetwork(sudokudata)	
	# NKT(network)
	v6 = network.variables[5]
	print("Check: {}".format(v6))
	removeAssignedNeighborsFromDomain(network, v6)
	print("Check: {}".format(v6))



	n6 = network.getNeighborsOfVariable(v6)
	
	print("neighbors {}".format(len(n6)))
	for i in n6:
		removeAssignedNeighborsFromDomain(network, i)
		print(i)




	# c6 includes v6
	c6 = getNakedPairConstraintsOfVariable(network, v6)
	print("gnpcov {}".format(len(c6)))
	for i in c6:
		print(i)
	print("Check: {}".format(v6))


if (__name__ == "__main__"):
	main()

