from gurobipy import *
     
# f = open('flow1.txt')
f = open('flow2.txt')
Board = [f.readline().strip()]
N = range(len(Board[0]))
for n in N[1:]:
    Board.append(f.readline().strip())
f.close()
C = []
Val = {(i,j):0 for i in N for j in N}
for n1 in N:
    for n2 in N:
        if Board[n1][n2] != '-':
            if Board[n1][n2] not in C:
                C.append(Board[n1][n2])
                Val[n1,n2] = len(C)
            else:
                Val[n1,n2] = -(C.index(Board[n1][n2])+1)
## End of STUB
K = range(len(C))
S = [(i,j) for i in N for j in N]
Sq = S

def Neighbour(i,j): #This is just a useful function we use all the time 
	'''Returns the up down left Right Neighbours of (i,j) '''
	tList = []
	if i > 0:
		tList.append((i-1,j))
	if i < len(Board[0]) - 1:
		tList.append((i+1, j))
	if j > 0:
		tList.append((i,j-1))
	if j < len(Board[0]) - 1:
		tList.append((i, j+1))
	return tList


Count = 0
def Callback(model,where):
	# if where == GRB.Callback.MESSAGE:
	# 	pass 
	# # print(Count)
	if where==GRB.Callback.MIPSOL:
		nadded = 0 
		XD = {(s1,s2,k): m.cbGetSolution(X[s1,s2,k]) for (s1,s2,k) in X} #Retrieve Values in Solution 
		for k in K: # For all Colours 
			for (s1,s2,k) in XD: # For viable keys of the solution 
				if XD[s1,s2,k]>0.1: # If the X value is used 
					tList = [s1] # set start of path 
					Upto = s2 #Next point in path 
					while Upto != s1 and Val[Upto] != -k-1: #If we have not cycled or reached the end yet 
						tList.append(Upto) #Updeate the next step 
						Flagg= False # Set flag to false 
						for s in S: # for all future points 
							if (Upto,s,k) in XD and XD[Upto,s,k]>0.1: # if that future point is used 
								Upto = s #update 
								Flagg = True #Path continues 
								break # Go To Line 69 
						if not Flagg: #Path does not continue, yet is not at an end 
							print('Incomplete Solution') # Should never get here 
					if Val[Upto[0],Upto[1]] != -k-1:
						nadded+=1
						m.cbLazy(quicksum(X[tList[i-1],tList[i],k] for i in range(len(tList)))<=len(tList)-1) #This is just a panic constrant 
						break

		if nadded ==0: # If we have never had to panic constraint 
			print('Solution') 
			for n1 in N:
				for n2 in N:
					if Val[n1,n2] != 0:
						boop=1 #Does Nothing 
					else: #If previous is 0 
						for s2 in Sq:
							for k in K:
								if ((n1,n2),s2,k) in X and XD[(n1,n2),s2,k] > 0.1: # if we go from previos to s with k 
									break #Pretty much if its a blankboi and we use it break 
			tList = [X[s1,s2,k] for (s1,s2,k) in X if XD[s1,s2,k] > 0.1]
			m.cbLazy(quicksum(tList) <= len(tList)-1) # Reduvce solution space by one 



numSols = 0

# This is a network flow prblem so. 
m = Model('Flow-2013')

X = {(s1,s2,k): m.addVar(vtype= GRB.BINARY) for s1 in S for s2 in Neighbour(s1[0],s1[1]) for k in K 
 if (Val[s2[0],s2[1]]==-k-1 or Val[s2[0],s2[1]] == 0) and (Val[s1[0],s1[1]]==k+1 or Val[s1[0],s1[1]] == 0)} # Only allow k if its a blank square of a sink/node

# m.setObjective(quicksum(X[s1,s2,k]for s1 in S for s2 in S for k in K if (s1,s2,k) in X),GRB.MINIMIZE)

#USE ALL SOURCES 
# Source = {(s1):m.addConstr(quicksum(X[s1,s2,k] for s2 in Neighbour(s1[0],s1[1]) for k in K if )==1 ) for s1 in S if Val[s1[0],s1[1]]>=0}
Source = {(s1):m.addConstr(quicksum(X[s1,s2,k] for s2 in S for k in K if (s1,s2,k) in X )==1 ) for s1 in S if Val[s1[0],s1[1]]>=0}


#Use All Sinks
Sinks = {(s2):m.addConstr(quicksum(X[s1,s2,k] for s1 in S for k in K if (s1,s2,k) in X)==1) for s2 in S if Val[s2[0],s2[1]]<=0 }

#Conserve Flow 
Conserve = {(s1,k): m.addConstr(quicksum(X[s1,s2,k] for s2 in S if (s1,s2,k) in X) ==
	quicksum(X[s2,s1,k] for s2 in S if (s2,s1,k) in X)) for k in K for s1 in S if Val[s1[0],s1[1]]==0}
m.setParam('LazyConstraints',1)

m.optimize(Callback)

path = {}
for k in K:
	path[k] = []
print(Board)
for (s1,s2,k) in X:
	if X[s1,s2,k].x>0.99:
		path[k].append((s1,s2))

print(path[1])