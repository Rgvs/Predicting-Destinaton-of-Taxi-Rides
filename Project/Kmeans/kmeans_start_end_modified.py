'''
Created at Jan 31st
Modified Feb 5th
Modified Feb 16th   model2: using 3d matrix to store start transiton end probabilites with kmeans
modified Feb 23rd
'''
import numpy as np
import re
from collections import OrderedDict
from itertools import izip
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
import json
from math import radians, cos, sin, asin, sqrt, ceil

class Dbscan:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['calltype_A']
        
    def db(self):
        
        number=0
        X=[]
        start=[]
        trans=[]
        end=[]
        new_total_distance=0.0
        total_distance=0.0
        f1 = open('../New Model/K_start_Kaggle_CA.txt' ,'r')
        st=f1.read().split('\n')
        for coordinates in st:
            coordinates=coordinates.split()
            try:
                start.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        f1 = open('../New Model/K_end_Kaggle_CA.txt' ,'r')
        e=f1.read().split('\n')
        for coordinates in e:
            coordinates=coordinates.split()
            try:
                end.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        label_start=-1 
        trips=0
        
        # matrix creation for training data 	
        count1=len(start) #start
        count3=len(end) #destination

        Matrix = [[0.0 for x in range(0,len(end)+1)] for y in range(0,len(start))]

        for line in izip(open('../New Model/trainA3.txt')):   ####need this fileeeee
            
            #print type(var)
            var=list(line[0].split())
            print var[0],var[-1],len(start),len(end)
        
            Matrix[int(var[0])][int(var[-1])] += 1.0
        
        #storing sum for each starting point
        for i in range(0,len(start)):
            add=0.0
            for j in range(0, len(end)):
                add+=Matrix[i][j]
            Matrix[i][len(end)]=add
            
        #changing count to probabilities
        for i in range(0,len(start)):
            for j in range(0, len(end)):
                try:
                    Matrix[i][j]=Matrix[i][j]/Matrix[i][len(end)]
                except:
                    pass
        u=g=bad=gg=uu=bb=0
        for tup in self.mongo_train.find( { '$and':[{'TIME.dayofyear': {'$lt': 277 } }, {'TIME.dayofyear': {'$gte': 270 } },{'DIRTY':0} ]}):
            # Generate sample data
            #print "yes"
            number=number+1
            if number%1000==0:
                print number
            #if number== 10000:
            #    break
            if len(tup["POLYLINE"]) < 20:
                continue
            trips = trips + 1    
            x1= float(tup["POLYLINE"][0][0])
            y1= float(tup["POLYLINE"][0][1])
            #print tup["POLY"]
            
            ###need a new file for starting clusters
            mini=10000000
            label_count = -1
            j=0
            for line in start:
                a=line[0]
                b=line[1]
                distance=haversine( a, b, x1, y1)
                if(mini>distance):
                    mini = distance
                    support_x = a
                    support_y = b
                    label_count = j
                    #print a,b,x1,y1
                j= j+1
                
            
            
                
            #finding destination based on maximum probabilty from matrix
            #label_start=182
               # need this filee
            
            
            
            largest=-1.5
            destination=0
            #print label_count
            for j in range(0, len(end)):
                if(largest < Matrix[label_count][j]):
                    #print Matrix[label_count][j]
                    #print type(j)
                    destination=int(j)
                    largest = Matrix[label_count][j]
            x_c=0.0
            y_c=0.0
            for j in range(0, len(end)):
                if(Matrix[label_count][j]!=0):
                    #print j
                    #print Matrix[label_start][label_trans]
                    f=end[j]
                    #print Matrix[label_start][label_trans][j], f
                    x_c += Matrix[label_count][j] * float(f[0])
                    y_c += Matrix[label_count][j] * float(f[1])
            #print x_c,y_c
            x_last = float(tup["POLYLINE"][-1][0])
            y_last = float(tup["POLYLINE"][-1][1])
            if x_c==0.0:
                trips-=1
                print destination
                continue
            new_distance=haversine( x_c, y_c, x_last, y_last)
            
            #break
            #verification
            x_last = float(tup["POLYLINE"][-1][0])
            y_last = float(tup["POLYLINE"][-1][1])
            mini=10000000
            label_count = destination
            line = end[label_count]
            #print f1
            a=line[0]
            b=line[1]
            total_distance=total_distance + haversine( a, b, x_last, y_last)
            new_total_distance+=new_distance
            if new_distance < 2000:
                g+=1
            elif new_distance < 5000:
                bad+=1
            else:
                u+=1
            if haversine( a, b, x_last, y_last) < 2000:
                gg+=1
            elif haversine( a, b, x_last, y_last) < 5000:
                bb+=1
            else:
                uu+=1
            print total_distance/trips,gg,bb,uu
            print new_total_distance/trips,g,bad,uu,trips,number
            
            
            #finding 5 closest destinations to transition points
            '''
            d=[0.0,0.0,0.0,0.0,0.0]
            e=[-1,-1,-1,-1,-1]
            for j in range(0,5):
                d[j]=Matrix[label_start][j]
                e[j]=j
  
            for j in range(5,count2): 
                val, idx = min((val, idx) for (idx, val) in enumerate(d))
                if Matrix[label_start][j]>val:
                    d[idx]=Matrix[label_start][j]
                    e[idx]=j
            dist=0
            least=1000000000.0
            last_x=0.0
            last_y=0.0 
            for j in range(0,5):
                #print d[j], Matrix[label_start][e[j]]
                if(d[j]!=0):
                    f3 = open('K_end.txt' ,'r')
                    f3= f3.read().split('\n')[e[j]]
                    line=f3.split()
                    #print line[2][:-1]
                    a=float(line[1])
                    b=float(line[2][:-1])
                    dist=haversine( a, b, x5, y5)
                    if dist<least:
                        least=dist
                        last_x=a
                        last_y=b
                        label_end=e[j]
            #print least, last_x, last_y
            
            #verification
            
            x_last = float(tup["POLY"][-1][0])
            y_last = float(tup["POLY"][-1][1])
            f1 = open('K_end.txt' ,'r') #need a new file end point support points
            mini=10000000
            f1 = f1.read().split('\n')[label_end]
            #print f1
            line=f1.split()
            #print line
            a=float(line[1])
            b=float(line[2][:-1])
            total_distance=total_distance + haversine( a, b, x_last, y_last)
            if trips%1000==0:
                print total_distance/trips
                
            '''
                
 #distance between (x1,y1) and all start support points       
def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km*1000


        
        


        
        
        
   
          
if __name__ == '__main__':
    cot = Dbscan()
    cot.db()
