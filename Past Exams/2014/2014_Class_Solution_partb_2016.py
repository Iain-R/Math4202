from gurobipy import *
import random
import itertools

# Size of board
nMax = 10
N = range(nMax)
# Max time
T = range(8)
V = range(2)

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


m = Model('Rescue')
X = [[[[m.addVar(vtype=GRB.BINARY, obj=C[i][j]) for t in T] for j in N] for i in N] for v in V]
m.update()
m.ModelSense = -1

# One cell per time period per vehicle
[m.addConstr(quicksum(X[v][i][j][t] for i in N for j in N)==1) for t in T for v in V]
# Each cell at most once
[m.addConstr(quicksum(X[v][i][j][t] for v in V for t in T)<=1) for i in N for j in N]

[m.addConstr(X[v][i][j][t]<=quicksum(X[v][n[0]][n[1]][t+1] for n in Neighbours(i,j))) for t in T[:-1] for i in N for j in N for v in V]
[m.addConstr(X[v][i][j][t+1]<=quicksum(X[v][n[0]][n[1]][t] for n in Neighbours(i,j))) for t in T[:-1] for i in N for j in N for v in V]

m.optimize()

for i in N:
    s = ''
    for j in N:
        for v in V:
            if sum(X[v][i][j][t].x for t in T) > 0.9:
                s += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[v]
                break
        else:
            s += '-'
    print s
    
