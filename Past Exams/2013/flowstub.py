from gurobipy import *
     
f = open('flow1.txt')
##f = open('flow2.txt')
Board = [f.readline().strip()]
N = range(len(Board[0]))
for n in N[1:]:
    Board.append(f.readline().strip())
f.close()
C = []
Val = {(i,j):0 for i in N for j in N}
for n1 in N:
    for n2 in N:
        if Board[n1][n2] <> '-':
            if Board[n1][n2] not in C:
                C.append(Board[n1][n2])
                Val[n1,n2] = len(C)
            else:
                Val[n1,n2] = -(C.index(Board[n1][n2])+1)
## End of STUB
