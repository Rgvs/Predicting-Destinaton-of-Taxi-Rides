import math

Matrix = [[0.0 for x in range(430)] for x in range(430)]
f1 = open('taxi_taxistand_matrix1.txt' ,'r')
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
        cos=0.0
        mod1=mod2=0.0    
        for j in range(0,65):
            cos+= (mat[i][j]*mat[k][j])
            mod1+=(mat[i][j]*mat[i][j])
            mod2+=(mat[k][j]*mat[k][j])
        
        Matrix[i][k]=cos/(math.sqrt(mod1)*math.sqrt(mod2))
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
fout2  = open("cosine.txt","w")
i=0
for line in f3:
    line1=line.split()
    #print 'a'
    fout2.write(str(line1[0]))
    fout2.write(" ")
    for j in range(0, 430):
        
        fout2.write(str(Matrix[i][j])+ " ")
    fout2.write("\n")
    i+=1    



# findiing taxi similarities
list_of_taxis = []
color_bit = []
#list_of_similar_taxis =[]
f1 = open('taxis.txt' ,'r')
number =-1
for line in f1:
    number +=1
    line1 = line.split()
    list_of_taxis.append(number)
    color_bit.append(0)
main_list = []

def main_func(list_of_taxis):
    
    similarity_list = initial_step(list_of_taxis)        ##function call
    main_list.append(similarity_list)
    list_of_taxis = [item for item in list_of_taxis if item not in similarity_list]
    while ( not list_of_taxis):
        main_func(list_of_taxis)
    



def initial_step (list_of_taxis1):
    list_of_similar_taxis =[]    
    count = 3
    for x in color_bit:
        count +=1
        if x ==0 :
            list_of_similar_taxis.append(list_of_taxis1[count])
            color_bit[count] =1
            break
    
    index = max_similarity_index(Matrix, list_of_similar_taxis,list_of_similar_taxis[count-4])
    #print index
    
    list_of_similar_taxis.append(list_of_taxis1[index])
    color_bit[index] =1
    similarity_list = similarity(index,Matrix,list_of_similar_taxis)     ## function call
    return similarity_list
    

def max_similarity_index(Matrix , list_of_similar_taxis, first_index ):
    index =0
    max_similarity = -1
#    if (max_similarity == 1.0):
#        max_similarity = Matrix[first_index][1]
#        index =1
    for i in range(1,430):
        if( float(Matrix[first_index][i]) > float(max_similarity) and not(float(Matrix[first_index][i]) == 1.0)):
            max_similarity = Matrix[first_index][i]
            index =i
            print max_similarity,first_index
    return index


def similarity(index,Matrix,list_of_similar_taxis):
    index = max_similarity_index(Matrix, list_of_similar_taxis,index)
    
    copy_list =list_of_similar_taxis[:]
    flag = 1
    for x in list_of_similar_taxis:
        if (Matrix[x][index] < 0.7):
            flag =0
            break
    if(flag == 1):
        list_of_similar_taxis.append(list_of_taxis[index])
        color_bit[index] = 1
    if(copy_list == list_of_similar_taxis):
        return list_of_similar_taxis
    else:
        #print index
        similarity(index,Matrix,list_of_similar_taxis)


    
main_func(list_of_taxis)
print list_of_taxis
print main_list
#initial_step(list_of_taxis)

