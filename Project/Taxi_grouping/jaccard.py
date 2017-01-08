Matrix = [[0.0 for x in range(430)] for x in range(430)]
f1 = open('taxi_taxistand_matrix.txt' ,'r')
i=0
mat=[[0.0 for x in range(65)] for y in range(430)]
for line in f1:
	line1=line.split()
	for k in range(0, 65):
		#print type(line1[k])		
		mat[i][k]=float(line1[k])
	i+=1

'''for i in range(0, 430):
	for j in range(0,65):
		print mat[i][j]
		print i,j
		
	print "\n"
'''
maxi=-1
i=0
j=0
k=0
for i in range(0, 430):
	for k in range(0, 430):	
		sim=0.0
		n=0.0	
		for j in range(0,65):
			if(mat[k][j]==mat[i][j]):
				sim+=1.0
			else:
				n+=1.0
	
		n+=sim
		Matrix[i][k]=sim/n
		if Matrix[i][k]==1.0:
			maxi+=1
print "done"
print maxi
'''for i in range(0, 430):
	for j in range(0,430):
		print Matrix[i][j],
		#print i,j
		
	print "\n"
'''


f3 = open('taxis.txt' ,'r')
fout2  = open("jaccard.txt","w")
i=0
for line in f3:
	line1=line.split()
	print 'a'
	fout2.write(str(line1[0]))
	fout2.write(" ")
	for j in range(0, 430):
		fout2.write(str(Matrix[i][j])+ " ")
	fout2.write("\n")
	i+=1	
			
