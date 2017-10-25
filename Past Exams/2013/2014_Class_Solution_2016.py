from gurobipy import *
     
##f = open('flow1.txt')
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

def Adjacent(s1, s2):
    return abs(s1[0]-s2[0])+abs(s1[1]-s2[1]) == 1

K = range(len(C))
Sq = [(n1,n2) for n1 in N for n2 in N]
m = Model('Flow')
X = {(s1,s2,k): m.addVar(vtype='B') for s1 in Sq for s2 in Sq for k in K
     if Adjacent(s1, s2) and (Val[s1] == 0 or Val[s1] == k+1)
     and (Val[s2] == 0 or Val[s2] == -k-1)}
m.update()
# Outflow from "source"
[m.addConstr(quicksum(X[s1,s2,k] for s2 in Sq for k in K if (s1,s2,k) in X) == 1)
             for s1 in Sq if Val[s1]>=0]
# Inflow to "sink"
[m.addConstr(quicksum(X[s1,s2,k] for s1 in Sq for k in K if (s1,s2,k) in X) == 1)
             for s2 in Sq if Val[s2]<=0]
# Flow conservation
[m.addConstr(quicksum(X[s1,s2,k] for s2 in Sq if (s1,s2,k) in X) ==
             quicksum(X[s2,s1,k] for s2 in Sq if (s2,s1,k) in X))
 for k in K for s1 in Sq if Val[s1] == 0]

numSols = 0

def messageCB(m, where):
    if where == GRB.Callback.MESSAGE:
        pass #print m.cbGet(GRB.Callback.MSG_STRING),
    elif where == GRB.Callback.MIPSOL:
        nAdded = 0
        XVal = {(s1,s2,k): m.cbGetSolution(X[s1,s2,k]) for (s1,s2,k) in X}
        for k in K:
            ## Look for a loop            
            for (s1,s2,k) in XVal:
                if XVal[s1,s2,k] > 0.1:
                    tList = [s1]
                    upto = s2
                    while upto !=s1 and Val[upto] != -k-1:
                        tList.append(upto)
                        fUpdate = False
                        for s in Sq:
                            if (upto,s,k) in XVal and XVal[upto,s,k] > 0.1:
                                upto = s
                                fUpdate = True
                                break
                        if not fUpdate:
                            print ('Update error', s1, s2, upto)
                    if Val[upto] !=-k-1:
                        nAdded += 1
                        m.cbLazy(quicksum(X[tList[i-1],tList[i],k] for i in range(len(tList)))\
                                          <= len(tList)-1)
                        break
        ## Count the solutions                    
        if nAdded == 0:
            global numSols
            numSols += 1
            print ('Solution', numSols)
            for n1 in N:
                strAns = ''
                for n2 in N:
                    if Val[n1,n2] != 0:
                        strAns += Board[n1][n2]
                    else:
                        for s2 in Sq:
                            for k in K:
                                if ((n1,n2),s2,k) in X and XVal[(n1,n2),s2,k] > 0.1:
                                    strAns += C[k]
                                    break
                print (strAns)
            tList = [X[s1,s2,k] for (s1,s2,k) in X if XVal[s1,s2,k] > 0.1]
            m.cbLazy(quicksum(tList) <= len(tList)-1)
    
m.setParam("LazyConstraints", 1)
m.setParam("DualReductions", 0)
m.optimize(messageCB)
