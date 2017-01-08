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

class Train_Test:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['160_calltype_C']
        
    def training(self):
        self.fin  = open("taxi_stand_4.txt","r")
        self.taxis=[]
        for line in self.fin:
            line=line.split()
            self.taxis.append(int(line[0]))
        number=0
        X=[]
        self.start=[]
        self.trans=[]
        self.end=[]
        f1 = open('K_start_CC.txt' ,'r')
        st=f1.read().split('\n')
        for coordinates in st:
            coordinates=coordinates.split()
            try:
                self.start.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        f1 = open('K_n_transition_K_CC.txt' ,'r')
        t=f1.read().split('\n')
        for coordinates in t:
            coordinates=coordinates.split()
            try:
                self.trans.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        f1 = open('K_end_CC.txt' ,'r')
        e=f1.read().split('\n')
        for coordinates in e:
            coordinates=coordinates.split()
            try:
                self.end.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        trips=0
        # matrix creation for training data     
        count1=250 #start
        count2=500 #tansition
        count3=250 #destination
        
        self.Matrix = [[[0.0 for k in range(0,count3+1)] for j in range(0,count2)] for i in range(0, count1)]
        for tup in self.mongo_train.find({"TIME.month":{"$ne":1} }):
            # Generate sample data
            #print "yes"
            number=number+1
            if number%1000==0:
                print number,trips
            #if number== 5000:
            #    break
            if len(tup["POLYLINE"])/4 < 8:
                continue
            flag =0
            for line in self.taxis:
                #print line[0],tup["TAXI_ID"]
                if(tup["TAXI_ID"] == int(line)):
                    flag =1
                    break
            if(flag == 0):
                continue
            trips = trips + 1
            minimun = 1000000000
            start_index = 0
            end_index =0
            trans_index =0 
            i =-1
            for coordinates in self.start:
                i+=1
                distance = haversine(coordinates[1],coordinates[0],float(tup["POLYLINE"][0][1]),float(tup["POLYLINE"][0][0]))
                if(minimun > distance):
                    minimum = distance
                    start_index = i
            i = -1
            minimun = 1000000000
            for coordinates in self.end:
                i+=1
                distance = haversine(coordinates[1],coordinates[0],float(tup["POLYLINE"][-1][1]),float(tup["POLYLINE"][-1][0]))
                if(minimun > distance):
                    minimum = distance
                    end_index = i
            for coordinates in tup["POLYLINE"][1:-1]:
                i = -1
                minimun = 1000000000
                for coord in self.trans:
                    i +=1
                    distance = haversine(coord[1],coord[0],float(coordinates[1]),float(coordinates[0]))
                    if(minimum > distance):
                        minimum = distance
                        trans_index = i
                self.Matrix[start_index][trans_index][end_index]+=1
        #storing sum for each starting point
        for i in range(0,count1):
            for j in range(0, count2):
                add=0.0
                for k in range(0, count3):
                    add+=self.Matrix[i][j][k]
                self.Matrix[i][j][count3]=add
            
        #changing count to probabilities
        for i in range(0,count1):
            for j in range(0, count2):
                for k in range(0, count3):
                    if(self.Matrix[i][j][count3]!=0):
                        self.Matrix[i][j][k]=self.Matrix[i][j][k]/self.Matrix[i][j][count3]
    def testing(self):
        number=0
        label_start=-1
        total_distance = 0.0 
        trips=0
        MISSING=0
        total_distance_new = 0.0
        count_good=count_avg=count_bad=0
        for tup in self.mongo_train.find({'TIME.month': 1}):
            number=number+1
            if number%1000==0:
                print number
            flag =0
            for line in self.taxis:
                if(tup["TAXI_ID"] == int(line)):
                    flag =1
                    break
            if(flag == 0):
                continue
            #if number== 10000:
            #    break
            if len(tup["POLYLINE"])/4 < 8:
                continue
            trips = trips + 1    
            x1= float(tup["POLYLINE"][0][0])
            y1= float(tup["POLYLINE"][0][1])
            x_t= float(tup["POLYLINE"][13][0]) #getting transition
            y_t= float(tup["POLYLINE"][13][1])
            #print tup["POLY"]
            
            ###need a new file for starting clusters
            mini=10000000
            label_start = -1
            j=0
            for line in self.start:
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
            for line in self.trans:
                
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
            
            largest=-1.5
            destination=0
            
            x_c=0.0
            y_c=0.0
            for j in range(0, 250):
                if(self.Matrix[label_start][label_trans][j]!=0):
                    #print j
                    #print self.Matrix[label_start][label_trans]
                    #print len(end)
                    f=self.end[j]
                    print f
                    #print self.Matrix[label_start][label_trans][j], f
                    x_c += self.Matrix[label_start][label_trans][j] * float(f[0])
                    y_c += self.Matrix[label_start][label_trans][j] * float(f[1])
            #print x_c,y_c
            x_last = float(tup["POLYLINE"][-1][0])
            y_last = float(tup["POLYLINE"][-1][1])
            new_distance=haversine( x_c, y_c, x_last, y_last)
            
            
            for j in range(0, 250):
                if(largest < self.Matrix[label_start][label_trans][j]):
                    #print self.Matrix[label_start][j]
                    #print type(j)
                    destination=int(j)
                    largest = self.Matrix[label_start][label_trans][j]
            #print largest
            #print destination
              
            #verification
            x_last = float(tup["POLYLINE"][-1][0])
            y_last = float(tup["POLYLINE"][-1][1])
            mini=10000000
            line = self.end[destination]
            #print f1
            #print f1
            
            a=line[0]
            b=line[1]
            #print a,b
            #print haversine( a, b, x_last, y_last)
            if largest==0.0:
                #print largest
                trips-=1
                MISSING+=1
                continue
            if new_distance < 15000:
                total_distance_new+=haversine( x_c, y_c, x_last, y_last)
            else:
                print x_c,y_c,1
                trips-=1
                continue
            total_distance=total_distance + haversine( a, b, x_last, y_last)
            
            if new_distance <2000:
                count_good+=1
            elif new_distance <5000:
                count_avg+=1
            else:
                count_bad+=1    
            print total_distance/trips, haversine( a, b, x_last, y_last)
            print total_distance_new/trips, new_distance, count_good, count_avg, count_bad, tup['TIME']['dayofmonth'],MISSING
        print total_distance/trips
        print total_distance_new/trips, count_good, count_avg, count_bad,MISSING

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
    cot = Train_Test()
    cot.training()
    cot.testing()
