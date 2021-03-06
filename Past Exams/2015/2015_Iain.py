# Stub for MATH4202 2015 Prac exam

from gurobipy import *

# The data for the squares
Data1 = [
[0,0,0,0,0,0],
[3,2,3,2,2,2],
[0,0,2,3,2,2],
[2,0,2,2,0,0],
[0,2,3,0,2,2],
[2,3,0,2,0,4]
]

Data2 = [
[3,2,2,3,2,1,3,2,2,0,2,0],
[2,3,2,3,2,0,2,3,2,3,2,3],
[0,1,3,1,2,2,0,1,3,1,2,2],
[1,1,0,1,3,1,1,1,0,3,0,1],
[2,2,1,3,3,1,2,2,1,3,3,1],
[3,2,1,1,2,2,3,2,1,1,2,2],
[3,2,2,1,2,0,3,2,2,0,2,0],
[2,3,2,3,2,2,2,3,2,3,2,0],
[0,1,3,1,2,2,0,1,3,1,2,2],
[1,1,0,0,2,1,1,1,1,0,2,1],
[2,2,1,3,3,1,2,2,1,3,3,1],
[3,2,1,1,2,2,3,2,1,1,2,2]
]

# Change this next line to test with Data1 or Data2
Data = Data1

# The size of the square
N = range(len(Data))

SOut = [(i,j) for i in N for j in N if Data[i][j]>0]
SIn = [(i,j) for i in N for j in N]


T = range(len(SOut))
maxT = T[-1]+1

def MoveTo(s):
    # Return the squares we can move to from square s
    retList = []
    i,j = s
    d = Data[i][j]
    for di in [-d,0,d]:
        for dj in [-d,0,d]:
            if i+di>=0 and i+di<=N[-1] and j+dj>=0 and j+dj<=N[-1] and (di!=0 or dj!=0):
                retList.append((i+di,j+dj))
    return retList

# Set this to True to test the PartB code, or false for the PartD code
PartB = True

def Callback(model,where):
    if where == GRB.Callback.MIPSOL:
        XD =  {(s1,s2): m.cbGetSolution(X[s1,s2]) for (s1,s2) in X} #Retrieve Values in Solution 
        for (s1,s2) in XD:
            if XD[s1,s2]>0.1:
                start = s1:
                tList = [s1]
                UpTo = s2
                Next = [MoveTo(s1) if (s1,MoveTo(s1)) in XD] 
                while UpTo!=start and len(Next)>0:




def GetValues1(model,VDict):
    return {k:v for (k,v) in zip(VDict.keys(), model.cbGetSolution(VDict.values()))if v > 0.99}#(key) of used value 
                
def Callback(model,where):
    if where==GRB.Callback.MIPSOL:
            # Extract the variables that are 1
        XD = GetValues1(model,X)
            #print(XD)
            # For each starting square, look for cycles
        for k in XD: #For Movement (s1,s2) ==  k
            Start = k[0] 
            tList = [Start]
            Upto = k[1]
            while Upto!=Start: 
                tList.append(Upto) #Include current node in list 
                    # We move one or zero (end of chain) squares
                NextMoves = [k for k in XD if k[0]==Upto] #Potential moces that start where we are up to(continue the path )
                if len(NextMoves)==0: #If this is empty we are done 
                    break
                else:
                    Upto = NextMoves[0][1] # if we have next moves just check the first one
                # If we got back to the start we have a cycle
            if Upto==Start:
                    # Cycle - need to add lazy constraint
                print('Cycle', tList)
                model.cbLazy(quicksum(X[s1,s2] for s1 in tList for s2 in tList if (s1,s2) in X)<=len(tList)-1)



if PartB:
    # Put the Part B code here.
    #This is like a time step flow thing 
    m = Model("Part B ")
    X = {(s1,s2,t):m.addVar( vtype = GRB.BINARY) for s1 in SOut for s2 in MoveTo(s1) for t in T}

    Move_One_At_A_Time = {(t):m.addConstr(quicksum(X[s1,s2,t] for s1 in SOut for s2 in MoveTo(s1)) ==1) for t in T}

    Dont_Move_Twice = {(s1):m.addConstr(quicksum(X[s1,s2,t] for s2 in MoveTo(s1) for t in T) ==1) for s1 in SOut}

    MaxOneMoveEachEnd = {
        (s2): m.addConstr(quicksum(X[s1,s2,t] for s1 in SOut for t in T if (s1,s2,t) in X)<=1)  #Each Point can be moved to at most once
        for s2 in SIn}

    DontMoveInUntilEmpty = {
        (s1,t): m.addConstr(quicksum(X[s2,s1,t] for s2 in SOut if (s2,s1,t) in X) # For Tiles that can move from Source to Other Source  
                    <=quicksum(X[s1,s2,td] for s2 in MoveTo(s1) for td in T[:t])) #Dont Until Thta source is empty 
        for s1 in SOut for t in T} #This is only so you dont move into a previously occupied tile until it moves 
    m.optimize()
else:
    # Put the Part D code here

    #Do B But now we want to get Rid of the concept of Time 
       m = Model("Part D")
       m.setParam('LazyConstraints',1)
    X = {(s1,s2):m.addVar( vtype = GRB.BINARY) for s1 in SOut for s2 in MoveTo(s1)}


    Dont_Move_Twice = {(s1):m.addConstr(quicksum(X[s1,s2,t] for s2 in MoveTo(s1)) ==1) for s1 in SOut}

    MaxOneMoveEachEnd = {
        (s2): m.addConstr(quicksum(X[s1,s2] for s1 in SOut if (s1,s2) in X)<=1)  #Each Point can be moved to at most once
        for s2 in SIn}

 

    m.optimize(Callback)