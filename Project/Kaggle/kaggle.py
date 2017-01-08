'''
Created at Jan 31st
Modified Feb 5th
Modified Feb 16th   model2: using 3d matrix to store start transiton end probabilites with kmeans
modified Feb 23rd
Modified Feb 29th
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
        self.mongo_test = self.mongo_db['cleantest_160mts']
        #self.mongo_train = self.mongo_db['cthrvt_160_1min']
        
    def db(self):
        myfile = open("myfile.csv", "a")
        number=0
        X=[]
        start=[]
        trans=[]
        end=[]
        '''
        f1 = open('../New Model/K_start_Kaggle_CA.txt' ,'r')
        st=f1.read().split('\n')
        for coordinates in st:
            coordinates=coordinates.split()
            
            try:
                start.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                #print coordinates
                pass
        '''
        metadata=open("metaData_taxistand.csv","r")
        taxi=[[0.0,0.0]]
        line=metadata.readline()
        for line in metadata:
            line =line.split(",")
            taxi.append( [ float (line[3][:-1]), float(line[2]) ] )
        start=taxi
        
        #myfile.write("TRIP_ID,LATITUDE,LONGITUDE"+"\n")
        myfile.write("\n")
        f1 = open('../New Model/K_end_Kaggle_CB.txt' ,'r')
        e=f1.read().split('\n')
        for coordinates in e:
            coordinates=coordinates.split()
            try:
                end.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                #print coordinates
                pass
        f1 = open('../New Model/K_transition_Kaggle_CB.txt' ,'r')
        t=f1.read().split('\n')
        for coordinates in t:
            coordinates=coordinates.split()
            try:
                trans.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                #print coordinates
                pass
        
        label_start=-1 
        total_distance = 0.0 
        trips=0
        total_distance_new = 0.0
        # matrix creation for training data 
        count1=len(start)+1 #start
        count2=500 #tansition
        count3=len(end) #destination

        Matrix = [[[0.0 for k in range(0,count3+1)] for j in range(0,count2)] for i in range(0, count1)]
        for line in izip(open('../New Model/trainB1.txt')):   ####need this fileeeee
            
            #print type(var)
            var=list(line[0].split())
            #print var
            for j in range(1,len(var)-1):
                #print var[0],count1
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
        for tup in self.mongo_test.find({'CALL_TYPE': 'B'} ):
            # Generate sample data
            #print "yes"
            trips = trips + 1
            if len(tup["POLYLINE"])==0:
                myfile.write( str(tup["TRIP_ID"])+','+str(41.145)+','+str(-8.61)+"\n")
                #myfile.write("\n")
                continue
            x1= float(tup["POLYLINE"][0][0])
            y1= float(tup["POLYLINE"][0][1])
            
            #if len(tup["POLYLINE"]) < 20:
            x_t= float(tup["POLYLINE"][-1][0]) #getting transition
            y_t= float(tup["POLYLINE"][-1][1])
            #else len(tup["POLYLINE"])<300:
            #    x_t= float(tup["POLYLINE"][19][0]) #getting transition
            #    y_t= float(tup["POLYLINE"][19][1])
            #else :
            #    myfile.write( str(tup["TRIP_ID"])+','+str(tup["POLYLINE"][-1][1])+','+str(tup["POLYLINE"][-1][0])+"\n")
                #myfile.write("\n")
            #    continue
            #print tup["POLY"]
            

            ###need a new file for starting clusters
            mini=10000000
            label_start = -1
            
            j=0
            for line in start:
                a=line[0]
                b=line[1]
                distance=haversine( a, b, x1, y1)
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
                    
            if (x_c!=0.0):
  
                myfile.write(str(tup["TRIP_ID"])+','+str(y_c)+','+str(x_c)+ "\n")
                #myfile.write("\n")
            else :
                x_t1= float(tup["POLYLINE"][len(tup["POLYLINE"])/2][0]) #getting transition
                y_t1= float(tup["POLYLINE"][len(tup["POLYLINE"])/2][1])
                mini=10000000
                label_trans = -1
                j=0
                for line in trans:
                    
                    #print line[2]
                    a=line[0]
                    
                    b=line[1]
                    #print a,b
                    distance=haversine( a, b, x_t1, y_t1)
                    if(mini>distance):
                        mini = distance
                        support_x = a
                        support_y = b
                        label_trans = j
                        #print a,b,x1,y1
                    j= j+1
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
                if (x_c!=0.0):
                    myfile.write(str(tup["TRIP_ID"])+','+str(y_c)+','+str(x_c)+ "\n")
                else:
                    myfile.write(str(tup["TRIP_ID"])+','+str(y_t)+','+str(x_t)+"\n")
               #myfile.write("\n")
            
            
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
