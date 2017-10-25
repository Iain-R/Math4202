import gurobipy as * 

# Do Data Shit 
def Neighbour(i,j): #This is just a useful function we use all the time 
	'''Returns the up down left Right Neighbours of (i,j) '''
	tList = []
	if i > 0:
		tList.append((i-1,j))
	if i < nMax - 1:
		tList.append((i+1, j))
	if j > 0:
		tList.append((i,j-1))
	if j < nMax - 1:
		tList.append((i, j+1))
	return tList


def GetValues1(model,VDict):
	'''Returns the current variables in the model if they are greater than 1'''
	return {k:v for (k,v) in zip(VDict.keys(), model.cbGetSolution(VDict.values())) if v > 0.99}
def Callback(model,where):
	''' This Callback Function specifically looks for cycles but thats like 99% of what we do with lazy constraints'''
	if where==GRB.Callback.MIPSOL:
        # Extract the variables that are 1
		XD = GetValues1(model,X)
        #print(XD)
        # For each starting square, look for cycles
		for k in XD: #For Solution in Model
			Start = k[0] #Solution start 
			tList = [Start] # Temp List 
			Upto = k[1] # Next node
			while Upto!=Start: #If the next node is not the start, we have not yet hit a cycle 
				tList.append(Upto) #Add to list 
                # We move one or zero (end of chain) squares
				NextMoves = [k for k in XD if k[0]==Upto] # Where do we go from here 
				if len(NextMoves)==0: # if we have checked the entire chain
					break
				else:
					Upto = NextMoves[0][1] # Go to next point 
            # If we got back to the start we have a cycle
			if Upto==Start: # OH SHIT we have hit a cycle better add a lazy constraint 
                # Cycle - need to add lazy constraint
				print('Cycle', tList)
				model.cbLazy(quicksum(X[s1,s2] for s1 in tList for s2 in tList if (s1,s2) in X) # If it cycles reduce its length by 1
				<=len(tList)-1)





m = Model('Network Flow Thingy')
m.setParam('LazyConstraints',1)

#Make sure you do the following constraints
# Flow in = flow out 
#Must leave all sources 
#Must enter all Sinks 


m.optimize(Callback)
