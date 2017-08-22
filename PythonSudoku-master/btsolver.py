import filereader
import gameboard
import variable
import domain
import trail
import constraint
import constraintnetwork
import time
import queue

'''
Thomas Tang and Westley Poon
'''

# dictionary mapping heuristic to number
'''

for example, to set the variable selection heuristic to MRV,
you would say,
self.setVariableSelectionHeuristic(VariableSelectionHeuristic['MinimumRemainingValue'])
this is needed when you have more than one heuristic to break ties or use one over the other in precedence.
you can also manually set the heuristics in the main.py file when reading the parameters
as the primary heuristics to use and then break ties within the functions you implement
It follows similarly to the other heuristics and chekcs
'''
VariableSelectionHeuristic = {'None': 0, 'MRV': 1, 'DH': 2} #, 'MRV2': 3}
ValueSelectionHeuristic = {'None': 0, 'LCV': 1}
ConsistencyCheck = {'None': 0, 'ForwardChecking': 1, 'ArcConsistency': 2}
HeuristicCheck = {'None': 0, 'NKP': 1, 'NKT': 2}


class BTSolver:
    "Backtracking solver"

    ######### Constructors Method #########
    def __init__(self, gb):
        self.network = filereader.GameBoardToConstraintNetwork(gb)
        self.trail = trail.masterTrailVariable
        self.hassolution = False
        self.gameboard = gb

        self.numAssignments = 0
        self.numBacktracks = 0
        self.preprocessing_startTime = 0
        self.preprocessing_endTime = 0
        self.startTime = None
        self.endTime = None

        self.varHeuristics = 0  # refers to which variable selection heuristic in use(0 means default, 1 means MRV, 2 means DEGREE)
        self.valHeuristics = 0  # refers to which value selection heuristic in use(0 means default, 1 means LCV)
        self.cChecks = 0  # refers to which consistency check will be run(0 for backtracking, 1 for forward checking, 2 for arc consistency)
        self.heuristicChecks = 0
        # self.runCheckOnce = False
        self.tokens = []  # tokens(heuristics to use)

    ######### Modifiers Method #########


    def setTokens(self, tokens):
        ''' set the set of heuristics to be taken into consideration'''
        self.tokens = tokens

    def setVariableSelectionHeuristic(self, vsh):
        '''modify the variable selection heuristic'''
        self.varHeuristics = vsh

    def setValueSelectionHeuristic(self, vsh):
        '''modify the value selection heuristic'''
        self.valHeuristics = vsh

    def setConsistencyChecks(self, cc):
        '''modify the consistency check'''
        self.cChecks = cc

    def setHeuristicChecks(self, hc):
        '''modify the heurisic check (naked pairs and triples)'''
        self.heuristicChecks += hc

    ######### Accessors Method #########
    def getSolution(self):
        return self.gameboard

    # @return time required for the solver to attain in seconds
    def getTimeTaken(self):
        return self.endTime - self.startTime

    ######### Helper Method #########
    def checkConsistency(self):
        """
        	which consistency check to run but it is up to you when implementing 
        	the heuristics to break ties using the other heuristics passed in
        """
        if self.cChecks == 0:
            return self.assignmentsCheck()
        elif self.cChecks == 1:
            return self.forwardChecking()
        elif self.cChecks == 2:
            return self.arcConsistency()
        else:
            return self.assignmentsCheck()

    def checkHeuristics(self):
        if self.heuristicChecks == 1:
            return self.nakedPairs()
        elif self.heuristicChecks == 2:
            return self.nakedTriples()
        elif self.heuristicChecks == 3:
            return self.nakedPairs() and self.nakedTriples()
        else:
            return True    

    def assignmentsCheck(self):
        """
            default consistency check. Ensures no two variables are assigned to the same value.
            @return true if consistent, false otherwise.
        """
        for v in self.network.variables:
            if v.isAssigned():
                for vOther in self.network.getNeighborsOfVariable(v):
                    if v.getAssignment() == vOther.getAssignment():
                        return False
        return True

    def nakedPairs(self):
        """
           naked pairs heuristic.
        """
        for v in self.network.variables:
        	if not v.isAssigned():
        		for i in self.getNakedPairConstraintsOfVariable(v):
        			if not i.isAssigned():
        				if v.domain.size() == 2 and v != i and i.domain.size() == 2:
        					if i.domain.values[0] == v.domain.values[0] and i.domain.values[1] == v.domain.values[1]:
        						self.reduceDomainsWithNakedPair((v, i))

        return True

    def getNakedPairConstraintsOfVariable(self, v):
    	elim_set = set()
    	for c in self.network.getConstraintsContainingVariable(v):
    		for v in c.vars:
    			if not v.isAssigned():
    				self.eliminateDomainOfVariable(v)
    				elim_set.add(v)
    	return elim_set 
  
    def eliminateDomainOfVariable(self, v):
    	neighbors = self.network.getNeighborsOfVariable(v)
    	for n in neighbors:
    		if n.isAssigned():
    			if n.domain.values[0] in v.domain.values:
    				v.removeValueFromDomain(n.domain.values[0])
    	return v


    def reduceDomainsWithNakedPair(self, nkp): #nkp is a 2-tuple
    	"""
    		TODO:	For only the neighbors of BOTH nkp values, remove their domain values from their neighbors
    	"""
    	union_set = set()
    	n1 = self.network.getNeighborsOfVariable(nkp[0])
    	n2 = self.network.getNeighborsOfVariable(nkp[1])
    	for v in n1:
    		if v in n2:
    			union_set.add(v)
    	for v in union_set:
    		if v != nkp[0] and v != nkp[1]:
    			if nkp[0].domain.values[0] in v.domain.values:
    				v.removeValueFromDomain(nkp[0].domain.values[0])
    			if nkp[0].domain.values[1] in v.domain.values:
    				v.removeValueFromDomain(nkp[0].domain.values[1])

    	


    def nakedTriples(self):
        """
           Naked triples heuristic.
        """
        for v in self.network.variables:
        	if not v.isAssigned():
        		elim_set = self.reducedDomainConstraintSet(v)
        		if v.size() == 3:
        			# print("\n~~ Elim set of {} ~~".format(v))
        			for i in elim_set:
        				# print("~~~~")
        				tup = (v,)
        				for l in i:
        					# print(l)
        					if not l.isAssigned() and l.size() < 4 and l != v and self.isSubset(v, l):
        						tup += (l,)
        						if len(tup) == 3:
        							# print("NAKER TRIPLE!")
        							self.reduceWithNakedTriple(tup)
        return True
    
    def isSubset(self, v, v2):
    	if v.size() < v2.size():
    		return False
    	for val in v2.Values():
    			if not val in v.Values():
    				return False
    	return True

    def reducedDomainConstraintSet(self, v):
    	cList = []
    	for c in self.network.getConstraintsContainingVariable(v): # [0] = row [1] = col [2] = blck
    		cSet = set()
    		for var in c.vars:
    			for n in self.network.getNeighborsOfVariable(var):
    				if n.isAssigned():
    					var.removeValueFromDomain(n.domain.values[0])
    			cSet.add(var)
    		cList.append(cSet)
    	return cList

    def reduceWithNakedTriple(self, nkt):
    	union_set = set()
    	for i in self.network.getNeighborsOfVariable(nkt[0]):
    		if i in self.network.getNeighborsOfVariable(nkt[1]) and i in self.network.getNeighborsOfVariable(nkt[2]):
    			union_set.add(i)
    	for v in union_set:
    		if v != nkt[0] and v != nkt[1] and v != nkt[2]:
    			if nkt[0].domain.values[0] in v.domain.values:
    				v.removeValueFromDomain(nkt[0].domain.values[0])
    			if nkt[0].domain.values[1] in v.domain.values:
    				v.removeValueFromDomain(nkt[0].domain.values[1])
    			if nkt[0].domain.values[2] in v.domain.values:
    				v.removeValueFromDomain(nkt[0].domain.values[2])


    def forwardChecking(self):
        """
           For every value assigned, remove that value from the domains of its neighbors
        """
        for v in self.network.variables:
        	if v.isAssigned():
        		for vOther in self.network.getNeighborsOfVariable(v):
        			if v.getAssignment() == vOther.getAssignment():
        				return False
        			vOther.removeValueFromDomain(v.domain.values[0])
        return True

    def arcConsistency(self): # Westley ACP
        """
            TODO: Implement Maintaining Arc Consistency.
        """
                # check for inconsistent assignments
        if not self.assignmentsCheck():
            return False

        arcs = queue.Queue()
        for v in self.network.variables:
            neighbors = self.network.getNeighborsOfVariable(v)
            for neighbor in neighbors:
                arcs.put((v, neighbor))

        while not arcs.empty():
            currentarc = arcs.get()
            x = currentarc[0]
            y = currentarc[1]

            # removing inconsistent values
            removed = False
            for xvalue in x.Values():
                remove = True
                for yvalue in y.Values():

                    # if there is a legal value in y's domain for the specific x value, should break
                    if xvalue != yvalue:
                        remove = False
                        break

                # if inconsistent, remove remains True and triggers removal of th value from x's domain
                if remove:
                    x.removeValueFromDomain(xvalue)
                    removed = True
                    if x.size() == 0:
                        return False

            # if x's domain changed, add all neighbor -> x arcs to queue
            if removed:
                xneighbors = self.network.getNeighborsOfVariable(x)
                for neighbor in xneighbors:
                    if not neighbor.isAssigned():
                        arcs.put((neighbor, x))

        return True

    def selectNextVariable(self):
        """
            Selects the next variable to check.
            @return next variable to check. null if there are no more variables to check.
        """
        if self.varHeuristics == 0:
            return self.getfirstUnassignedVariable()
        elif self.varHeuristics == 1:
            return self.getMRV()
        elif self.varHeuristics == 2:
            return self.getDegree()
        # elif self.varHeuristics == 3:
        #     return self.getMRV2()
        else:
            return self.getfirstUnassignedVariable()

    def getfirstUnassignedVariable(self):
        """
            default next variable selection heuristic. Selects the first unassigned variable.
            @return first unassigned variable. null if no variables are unassigned.
        """
        for v in self.network.variables:
            if not v.isAssigned():
                return v
        return None

    # def getMRV2(self): # Westley MRV

    # 	min_values = self.gameboard.N + 1
    # 	mrv = None
    # 	for v in self.network.variables:
    # 		if not v.isAssigned():
    # 			# if a variable's domain size is lower than the current min, it becomes the new min
    # 			if v.size() < min_values:
    # 				min_values = v.size()
    # 				mrv = v
    # 	return mrv

    def getMRV(self): # Thomas
        """
            @return variable with minimum remaining values that isn't assigned, null if all variables are assigned.
        """	
        templist = []
        for v in self.network.variables:
        	if not v.isAssigned():
        		templist.append((v, self.MRV_helper(v)))
        self.quicksort(templist)
        for tup in templist:
        	return tup[0]
        return None

    ##### MRV HELPERS ####
    def MRV_helper(self, v):	
    	"""
    			@returns a list of domain values after eliminating known / assigned values
    	"""
    	outlist = set() # initial set of domain values in temp list
    	for i in range(0, self.gameboard.N):
    		outlist.add(i+1)
    	list_of_constraints = self.network.getConstraintsContainingVariable(v)
    	for c in list_of_constraints: # for each constraint for variable v
    		for var in c.vars: # for each variable in the constraint
    			if var.isAssigned(): # if the variable is assigned (has only one value)
    				if var.domain.values[0] in outlist:
    					outlist.remove(var.domain.values[0]) #remove the value in the domain from the temp list
    	return list(outlist)


    def getDegree(self):
        """
            @return variable constrained by the most unassigned variables, null if all variables are assigned.
        """
        templist = []
        for v in self.network.variables:
        	if not v.isAssigned():
        		templist.append((v, self.DegreeHelper(v)))
        self.quicksort(templist)
        for tup in templist:
        	return tup[0]
        return None
	
    ##### DEGREE HELPERS ####
    def DegreeHelper(self, v):
	    	list_of_constraints = self.network.getConstraintsContainingVariable(v)
	    	outlist = set()
	    	for c in list_of_constraints:
	    		for var in c.vars:
	    			if not var.isAssigned():
	    				outlist.add(var)
	    	return list(outlist)

    """
			this quicksort is specifically for the tuple : (variable, comparator)
		"""
    def partition(self, array, begin, end):
		    pivot = begin
		    for i in range(begin+1, end+1):
		        if len(array[i][1]) <= len(array[begin][1]): # sorts values of array by length of domain list
		            pivot += 1
		            array[i], array[pivot] = array[pivot], array[i]
		    array[pivot], array[begin] = array[begin], array[pivot]
		    return pivot

    def quicksort(self, array, begin=0, end=None):
		    if end is None:
		        end = len(array) - 1
		    def _quicksort(array, begin, end):
		        if begin >= end:
		            return
		        pivot = self.partition(array, begin, end)
		        _quicksort(array, begin, pivot-1)
		        _quicksort(array, pivot+1, end)
		    return _quicksort(array, begin, end)
		

    def getNextValues(self, v):
        """
            Value Selection Heuristics. Orders the values in the domain of the variable
            passed as a parameter and returns them as a list.
            @return List of values in the domain of a variable in a specified order.
        """
        if self.valHeuristics == 0:
            return self.getValuesInOrder(v)
        elif self.valHeuristics == 1:
            return self.getValuesLCVOrder(v)
        else:
            return self.getValuesInOrder(v)


    def getValuesInOrder(self, v):
        """
            Default value ordering.
            @param v Variable whose values need to be ordered
            @return values ordered by lowest to highest.
        """
        values = v.domain.values
        return sorted(values)


    def getValuesLCVOrder(self, v):
        """
            LCV heuristic (least constraining)
            @return values ordered by number of constraints
        """
        lcvPairs = self.getLCV(v)
        self.quicksort2(lcvPairs)
        lcvList = []
        for i in lcvPairs:
        	lcvList.append(i[0])
        # lcvList.reverse()
        return lcvList

    def getLCV(self, v):
    	lcvPairList = []
    	for i in range(0, self.gameboard.N):
    		lcvPairList.append([i+1, 0])
    	list_of_constraints = self.network.getConstraintsContainingVariable(v)
    	for c in list_of_constraints:
    		for var in c.vars:
    			if var.isAssigned():
    				lcvPairList[var.domain.values[0] - 1][1] += 1
    	return lcvPairList

    def part2(self, array, begin, end):
    	pivot = begin
    	for i in range(begin+1, end+1):
    		if array[i][1] <= array[begin][1]:
    			pivot += 1
    			array[i], array[pivot] = array[pivot], array[i]
    	array[pivot], array[begin] = array[begin], array[pivot]
    	return pivot

    def quicksort2(self, array, begin=0, end=None):
    	if end is None:
    		end = len(array) - 1
    	def _quicksort(array, begin, end):
    		if begin >= end:
    			return
    		pivot = self.part2(array, begin, end)
    		_quicksort(array, begin, pivot-1)
    		_quicksort(array, pivot+1, end)
    	return _quicksort(array, begin, end)






    def success(self):
        """ Called when solver finds a solution """
        self.hassolution = True
        self.gameboard = filereader.ConstraintNetworkToGameBoard(self.network,
                                                                 self.gameboard.N,
                                                                 self.gameboard.p,
                                                                 self.gameboard.q)


    ######### Solver Method #########
    def solve(self):
        """ Method to start the solver """
        self.startTime = time.time()
        # try:
        # print(self.network)
        self.solveLevel(0)

        # except:
        # print("Error with variable selection heuristic.")
        self.endTime = time.time()
        # trail.masterTrailVariable.trailStack = []
        self.trail.trailStack = []


    def solveLevel(self, level):
        """
            Solver Level
            @param level How deep the solver is in its recursion.
            @throws VariableSelectionException
        contains some comments that can be uncommented for more in depth analysis
        """
        # print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")
        # print("BEFORE ANY SOLVE LEVEL START")
        # print(self.network)
        # print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

        if self.hassolution:
            return

        # Select unassigned variable
        v = self.selectNextVariable()
        # print("V SELECTED --> " + str(v))

        # check if the assigment is complete
        if (v == None):
            # print("!!! GETTING IN V == NONE !!!")
            for var in self.network.variables:
                if not var.isAssigned():
                    raise ValueError("Something happened with the variable selection heuristic")
            self.success()
            return

        # loop through the values of the variable being checked LCV
        # print("getNextValues(v): " + str(self.getNextValues(v)))
        for i in self.getNextValues(v):
            # print("next value to test --> " + str(i))
            self.trail.placeTrailMarker()

            # check a value
            # print("-->CALL v.updateDomain(domain.Domain(i)) to start to test next value.")
            v.updateDomain(domain.Domain(i))
            self.numAssignments += 1

            # move to the next assignment
            if self.checkConsistency() and self.checkHeuristics():
                self.solveLevel(level + 1)

            # if this assignment failed at any stage, backtrack
            if not self.hassolution:
                # print("=======================================")
                # print("AFTER PROCESSED:")
                # print(self.network)
                # print("================ ")
                # print("self.trail before revert change: ")
                for i in self.trail.trailStack:
                    pass
                    # print("variable --> " + str(i[0]))
                    # print("domain backup --> " + str(i[1]))
                # print("================= ")

                self.trail.undo()
                self.numBacktracks += 1
                # print("REVERT CHANGES:")
                # print(self.network)
                # print("================ ")
                # print("self.trail after revert change: ")
                for i in self.trail.trailStack:
                    pass
                    # print("variable --> " + str(i[0]))
                    # print("domain backup --> " + str(i[1]))
                # print("================= ")

            else:
                return
