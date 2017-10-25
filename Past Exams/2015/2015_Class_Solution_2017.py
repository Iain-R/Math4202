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
Data = Data2

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
PartB = False

if PartB:
    # Put the Part B code here.
    m = Model()
    X = {(s1,s2,t): m.addVar(vtype=GRB.BINARY)
        for s1 in SOut for s2 in MoveTo(s1) for t in T}
    OneMoveInEachTimeStep = {
        (t): m.addConstr(quicksum(X[s1,s2,t] for s1 in SOut for s2 in MoveTo(s1))==1)
        for t in T}    
    OneMoveEachStart = {
        (s1): m.addConstr(quicksum(X[s1,s2,t] for s2 in MoveTo(s1) for t in T)==1)
        for s1 in SOut}
    MaxOneMoveEachEnd = {
        (s2): m.addConstr(quicksum(X[s1,s2,t] for s1 in SOut for t in T if (s1,s2,t) in X)<=1)
        for s2 in SIn}
    DontMoveInUntilEmpty = {
        (s1,t): m.addConstr(quicksum(X[s2,s1,t] for s2 in SOut if (s2,s1,t) in X)
                    <=quicksum(X[s1,s2,td] for s2 in MoveTo(s1) for td in T[:t]))
        for s1 in SOut for t in T}
    m.optimize()
    for t in T:
        for s1 in SOut:
            for s2 in MoveTo(s1):
                if X[s1,s2,t].x > 0.9:
                    print(t,s1,s2)
                    
else:
    # Put the Part D code here
    m = Model()
    X = {(s1,s2): m.addVar(vtype=GRB.BINARY)
        for s1 in SOut for s2 in MoveTo(s1)}

    def GetValues1(model,VDict):
        return {k:v for (k,v) in zip(VDict.keys(), model.cbGetSolution(VDict.values()))
                if v > 0.99}
                
    def Callback(model,where):
        if where==GRB.Callback.MIPSOL:
            # Extract the variables that are 1
            XD = GetValues1(model,X)
            #print(XD)
            # For each starting square, look for cycles
            for k in XD:
                Start = k[0]
                tList = [Start]
                Upto = k[1]
                while Upto!=Start:
                    tList.append(Upto)
                    # We move one or zero (end of chain) squares
                    NextMoves = [k for k in XD if k[0]==Upto]
                    if len(NextMoves)==0:
                        break
                    else:
                        Upto = NextMoves[0][1]
                # If we got back to the start we have a cycle
                if Upto==Start:
                    # Cycle - need to add lazy constraint
                    print('Cycle', tList)
                    model.cbLazy(quicksum(X[s1,s2] for s1 in tList for s2 in tList if (s1,s2) in X)
                        <=len(tList)-1)

            
    OneMoveEachStart = {
        (s1): m.addConstr(quicksum(X[s1,s2] for s2 in MoveTo(s1))==1)
        for s1 in SOut}
    MaxOneMoveEachEnd = {
        (s2): m.addConstr(quicksum(X[s1,s2] for s1 in SOut if (s1,s2) in X)<=1)
        for s2 in SIn}
    m.setParam('LazyConstraints',1)
    m.optimize(Callback)
    for s1 in SOut:
        for s2 in MoveTo(s1):
            if X[s1,s2].x > 0.9:
                print(s1,s2)
