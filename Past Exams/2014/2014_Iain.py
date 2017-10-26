from gurobipy import *
import random
from tqdm import tqdm
# Size of board
nMax = 10
N = range(nMax)
# Max time
T = range(8)
# Number of vehicles
V = range(6)

def Neighbours(point):
    i=point[0]
    j=point[1]
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

for c in C:
    print (c)
Combo = []
def GenPath(end,past):
    if len(past) ==end:
        Combo.append(past)
        return None 
    for s in Neighbours(past[-1]):
        if s not in past:
            GenPath(end, past+[s])
print('Begining Sequence Generation ')
for i in N: 
    for j in N:
        GenPath(8, [(i,j)])

PathSet  = set(tuple(sorted(p)) for p in Combo)
Paths = [tuple(p) for p in PathSet]
print("Starting Model")
print("Setting Delta")
Delta = {}
for p in Paths:
    for i in N:
        for j in N :
                if (i,j) in p:
                    Delta[p,(i,j)] =1
                else:
                    Delta[p,(i,j)] =0

m= Model()
X = {(c): m.addVar(vtype = GRB.BINARY) for c in Paths}
Y = {(i,j): m.addVar(vtype = GRB.BINARY)  for i in N for j in N }

m.setObjective(quicksum(X[c]*C[p[0]][p[1]] for c in Paths for p in c ),GRB.MAXIMIZE)

# DontOverlap = {(c,i,j):m.addConstr(quicksum(X[c]*Delta[c,(i,j)] ) == 1)for c in Paths for i in N for j in N if (c,(i,j))in Delta }
Dont_Overlap = {(i,j):m.addConstr(quicksum(X[c]*Delta[c,(i,j)] for c in Paths )<=1) for i in N for j in N }
VehilcesOnce= {m.addConstr(quicksum(X[c] for c in Paths)==len(V))}

m.optimize()
v=0
for c in Paths:
        if X[c].x>0.9:
            v+=1
            print("\n Vehicle:\t",v,"  Path:\t",c)