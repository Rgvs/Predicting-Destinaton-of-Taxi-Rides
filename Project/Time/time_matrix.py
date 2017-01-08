import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('GTKAgg')
import random
import numpy as np
from matplotlib.legend_handler import HandlerLine2D
import matplotlib.patches as mpa
f=open("matrix.txt","r")
time_array = [[0 for x in range(250)] for x in range(4)]
count=-1
for line in f:
    count+=1
    line=line.split()
    i=0
    for k in line:
        print i,count
        time_array[count/6][i]+=int(k)
        i+=1

#print time_array
start_cluster=open("K_start_Kaggle_CA.txt","r")
start=[]
count=-1
for line in start_cluster:
    count +=1
    line = line.split()
    a = float(line[0])
    b = float(line[1])
    start.append([a,b])
point=[]
count=-1
C=[]
rowNum=-1
for row in time_array:
    rowNum+=1
    count=-1
    print rowNum
    for i in row:
        count+=1
        i= int(i)
        while(i>0):
            #print start[count][1]
            #print random.uniform( start[count][1]-0.0001 , start[count][1]+0.0001)
            point.append([ random.uniform( start[count][0]-0.001 , start[count][0]+0.001) , random.uniform( start[count][1]-0.001 , start[count][1]+0.001),rowNum ])
            #C.append(rowNum)
            i=i-10
    
point=np.array(point)
np.random.shuffle(point)
print point[:,1]
plt.scatter(point[:, 0], point[:, 1],c=point[:,2],s=50,marker="^",alpha=0.5)
recs=[]
class_colours=['r','lightblue','y','g']
for i in range(0,4):
    recs.append(mpa.Rectangle((0,0),1,1,fc=class_colours[i]))
plt.legend(recs,['0-6','6-12','12-18','18-24'],loc=4)
plt.savefig("time_6Hour.png",dpi = 1200)
plt.show()
