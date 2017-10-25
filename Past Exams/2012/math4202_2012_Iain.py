import math 
from gurobipy import * 
Items  = range(100,205,5)
Amounts = range(300,455,5)
# Items  = range(200,355,5)
# Amounts = range(500,805,5)
nitems = range(len(Items))
namount = range(len(Amounts))

# for a in Amounts:
Value = [i for i in Items]
Spend  =[i for i in Amounts]

m = Model()

X = {(f,i):m.addVar( vtype = GRB.BINARY) for f in nitems for i in namount}
# 1 if we use price 0 otherwise
Y = {(f):m.addVar( vtype = GRB.BINARY) for f in nitems}
m.setObjective(quicksum(Y[f] for f in nitems),GRB.MINIMIZE)

#Use as few items as possible 
Link = {(f):m.addConstr(quicksum(X[f,i] for i in namount)<=Y[f]*90000000000) for f in nitems}
AddToCost = {(i):
			m.addConstr(quicksum(X[f,i]*Value[f] for f in nitems) == Spend[i]) for i in namount}
m.optimize()

print('Menu\n')
print([Value[f] for f in nitems if Y[f].x> 0.9])