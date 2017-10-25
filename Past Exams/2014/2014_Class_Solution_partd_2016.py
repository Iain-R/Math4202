from gurobipy import *
import random

# Size of board
nMax = 10
N = range(nMax)
# Max time
T = range(8)
V = range(6)

def Neighbours(i,j):
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

random.seed(5)
C = [[random.randint(0,4) for j in N] for i in N]

pList = []

def Recurse(tList, n):
    if n == 0:
        pList.append(list(tList))
    else:
        for s in Neighbours(tList[-1][0], tList[-1][1]):
            if s not in tList:
                Recurse(tList+[s], n-1)

for i in N:
    for j in N:
        Recurse([(i,j)], len(T)-1)

print (len(pList))
pSet = set(tuple(sorted(p)) for p in pList)
pList = [list(p) for p in pSet]
print (len(pList))

m = Model('Rescue')
X = [m.addVar(vtype=GRB.BINARY, obj=sum(C[t[0]][t[1]] for t in p)) for p in pList]
m.update()
m.ModelSense = -1
# Choose the correct number of pieces
m.addConstr(quicksum(X)==len(V))
# Cover each square at most once
[m.addConstr(quicksum(x for x,p in zip(X,pList) if (i,j) in p)<=1) for i in N for j in N]
m.optimize()

Board = [['-' for j in N] for i in N]

v = 0
for x,p in zip(X,pList):
    if x.X > 0.9:
        for t in p:
            Board[t[0]][t[1]] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[v]
        v += 1

for i in N:
    print (''.join(Board[i]))

