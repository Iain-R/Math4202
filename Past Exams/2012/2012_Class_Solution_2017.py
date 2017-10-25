# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from gurobipy import *
import itertools

Items = range(100,205,5)
Amounts = range(300,455,5)
Items = range(200,355,5)
Amounts = range(500,805,5)

m = Model()

X = {i: m.addVar(vtype=GRB.BINARY) for i in Items}
Combo = {a:[] for a in Amounts}
for choose in (2,3):
    for k in itertools.combinations(Items,choose):
        Tot = sum(k)
        if Tot in Combo:
            Combo[Tot].append(k)
Z = {(a,k): m.addVar(vtype=GRB.BINARY) for a in Amounts for k in Combo[a]}
     
m.setObjective(quicksum(X[i] for i in Items))

HitAmounts = {
    a: m.addConstr(quicksum(Z[a,k] for k in Combo[a])>=1) 
    for a in Amounts}
    
OnlyUseChosenItems = {
    (k,a): m.addConstr(Z[a,k]<=X[i])
    for a in Amounts for k in Combo[a] for i in k}

for i in Items:
    X[i].BranchPriority = 1

m.optimize()     