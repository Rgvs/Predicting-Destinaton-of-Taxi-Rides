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
        f1 = open('../Db/db_start.txt' ,'r')
        st=f1.read().split('\n')
        for coordinates in st:
            coordinates=coordinates.split()
            
            try:
                start.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        f1 = open('../Db/db_end.txt' ,'r')
        e=f1.read().split('\n')
        for coordinates in e:
            coordinates=coordinates.split()
            try:
                end.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        f1 = open('../New Model/K_transition_Kaggle_CA.txt' ,'r')
        t=f1.read().split('\n')
        for coordinates in t:
            coordinates=coordinates.split()
            try:
                trans.append ([ float(coordinates[0]),float(coordinates[1])] )
                #print coordinates[0]
            except:
                pass
        
        label_start=-1 
        total_distance = 0.0 
        trips=0
        total_distance_new = 0.0
        # matrix creation for training data 
        count1=len(start) #start
        count2=500 #tansition
        count3=len(end) #destination

        Matrix = [[[0.0 for k in range(0,count3+1)] for j in range(0,count2)] for i in range(0, count1)]
        f1 = open('../Db/start_fixed.txt' ,'r')
        f2 = open('../Db/end_fixed.txt' ,'r')
        for line in izip(open('../New Model/trainA1.txt')):   ####need this fileeeee
            
            #print type(var)
            var=list(line[0].split())
            #print var
            var[0]=f1.readline()
            var[-1]=f2.readline()
            for j in range(1,len(var)-1):
                #print var[-1]
                if int(var[j]) != int(var[j-1]) and j!=1:
                    Matrix[int(var[0])][int(var[j])][int(var[-1])] += 1.0
            
        #storing sum for each starting point
        for i in range(0,count1):
            for j in range(0, count2):
                add=0.0
                for k in range(0, count3):
                    add+=Matrix[i][j][k]
                Matrix[i][j][count3]=add
            
        #changing count to probabilities
        for i in range(0,count1):
            for j in range(0, count2):
                for k in range(0, count3):
                    if(Matrix[i][j][count3]!=0):
                        Matrix[i][j][k]=Matrix[i][j][k]/Matrix[i][j][count3]
        #for tup in self.mongo_train.find( {"$and" : [ 
        #                                    { "$or": [ 
        #                                        {'TIME.month':6}, 
        #                                        {'TIME.month':6} 
        #                                        ] } , 
        #                                    {'CALL_TYPE': 'C'}
        #                                    ]}):
        u=g=bad=gg=uu=bb=0
        for tup in self.mongo_train.find({ '$and':[{'TIME.dayofyear': {'$lt': 277 } }, {'TIME.dayofyear': {'$gte': 270 } },{'DIRTY':0} ]}):
            number=number+1
            if number%1000==0:
                print number
            #if number== 10000:
            #    break
            if len(tup["POLYLINE"])< 21:
                continue
            trips = trips + 1    
            x1= float(tup["POLYLINE"][0][0])
            y1= float(tup["POLYLINE"][0][1])
            x_t= float(tup["POLYLINE"][15][0]) #getting transition
            y_t= float(tup["POLYLINE"][15][1])
            #print tup["POLY"]
            
            ###need a new file for starting clusters
            mini=10000000
            label_start = -1
            j=0
            for line in start:
                a=line[0]
                b=line[1]
                distance=(a-x1)*(a-x1) + (b-y1)*(b-y1)
                if(mini>distance):
                    mini = distance
                    support_x = a
                    support_y = b
                    label_start = j
                    #print a,b,x1,y1
                j= j+1
                
            ###need a new file for transition clusters
            mini=10000000
            label_trans = -1
            j=0
            for line in trans:
                
                #print line[2]
                a=line[0]
                
                b=line[1]
                #print a,b
                distance=haversine( a, b, x_t, y_t)
                if(mini>distance):
                    mini = distance
                    support_x = a
                    support_y = b
                    label_trans = j
                    #print a,b,x1,y1
                j= j+1    
    
            
                
            #finding destination based on maximum probabilty from matrix
            #label_start=182
               # need this filee
            
            
            
            largest=-1.5
            destination=0
            #print label_start
            #print Matrix[label_start][label_trans]
            
            x_c=0.0
            y_c=0.0
            for j in range(0, count3):
                if(Matrix[label_start][label_trans][j]!=0):
                    #print j
                    #print Matrix[label_start][label_trans]
                    f=end[j]
                    #print Matrix[label_start][label_trans][j], f
                    x_c += Matrix[label_start][label_trans][j] * float(f[0])
                    y_c += Matrix[label_start][label_trans][j] * float(f[1])
            #print x_c,y_c
            x_last = float(tup["POLYLINE"][-1][0])
            y_last = float(tup["POLYLINE"][-1][1])
            new_distance=haversine( x_c, y_c, x_last, y_last)
            
            
            for j in range(0, count3):
                if(largest < Matrix[label_start][label_trans][j]):
                    #print Matrix[label_start][j]
                    #print type(j)
                    destination=int(j)
                    largest = Matrix[label_start][label_trans][j]
                    
                    
            #print largest
            #print destination
              
            #verification
            
            x_last = float(tup["POLYLINE"][-1][0])
            y_last = float(tup["POLYLINE"][-1][1])
             # need this filee
            mini=10000000
            label_start = destination
            line = end[label_start]
            #print f1
            #print f1
            
            a=line[0]
            b=line[1]
            #print a,b
            #print haversine( a, b, x_last, y_last)
            if largest==0.0:
                print largest
                trips-=1
                continue
            total_distance=total_distance + haversine( a, b, x_last, y_last)
            if new_distance < 15000:
                total_distance_new+=haversine( x_c, y_c, x_last, y_last)
            else:
                print x_c,y_c
                trips-=1
                continue
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
            print total_distance_new/trips,g,bad,uu,trips,number
            
            
            #break
            
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
