# Here we want to generate a sequence of values and then consider these sequences for our 
# MIP because this is way faster 


def Neighbour(i,j): #This is just a useful function we use all the time 
	'''Returns the up down left Right Neighbours of (i,j) '''
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


Seq = []
def GenSequence(end, past):
	""" Generates all sequences recursivly and appends them to some value Seq"""
	if past[-1] == end:
		Seq.append(past)
		return None
	for n in Neighbour(past[-1][0],past[-1][1]):
		if n not in past:
			GenSequence(end, past+[n])

for i in N: 
	for j in N:
		GenSequence(end,[i,j])

Sset = set(tuple(sorted(k) for k in Seq)) #Gets Rid of duplicates
Sequence = [list(k) for k in Sset] #Makes it a list but now with now duplicates 

