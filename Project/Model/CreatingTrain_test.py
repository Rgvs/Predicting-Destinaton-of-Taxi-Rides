'''
Created on April 24th
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

class Creat_test_train:
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_train = self.mongo_db['calltype_C']
        self.start=[]
        self.trans=[]
        self.end=[]
        f1 = open('K_start_Kaggle_CC.txt' ,'r')
        st=f1.read().split('\n')
        for coordinates in st:
            coordinates=coordinates.split()
            try:
                self.start.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        f1 = open('K_transition_Kaggle_CC.txt' ,'r')
        t=f1.read().split('\n')
        for coordinates in t:
            coordinates=coordinates.split()
            try:
                self.trans.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        f1 = open('K_end_Kaggle_CC.txt' ,'r')
        e=f1.read().split('\n')
        for coordinates in e:
            coordinates=coordinates.split()
            try:
                self.end.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        
    def test(self):
        f=open("testC10.txt","w")
        f1=open("Actual_endC10.txt","w")
        f2=open("testCA10.txt","w")
        f3=open("Actual_endCA10.txt","w")
        f4=open("testCD10.txt","w")
        f5=open("Actual_endCD10.txt","w")        
        number=0
        for tup in self.mongo_train.find({ '$and':[{'TIME.dayofyear': {'$lt': 340 } }, {'TIME.dayofyear': {'$gte': 333 } },{'DIRTY':0} ]}):
            #print "yes"
            if len(tup["POLYLINE"]) <22:
                continue
            number+=1
            if number%1000==0:
                print number
                #if number==5000:
                #    break
            mini=10000000
            label_start = -1
            j=0
            for line in self.start:
                a=line[0]
                b=line[1]
                distance=haversine( a, b,tup['POLYLINE'][0][0] ,tup['POLYLINE'][0][1] )
                if(mini>distance):
                    mini = distance
                    support_x = a
                    support_y = b
                    label_start = j
                    #print a,b,x1,y1
                j= j+1
            label_transition=[]
            for coordinates in tup["POLYLINE"][1:20]:
                mini=10000000
                label_trans = -1
                j=0
                for line in self.trans:
                    
                    #print line[2]
                    a=line[0]
                    
                    b=line[1]
                    distance=haversine( a, b, coordinates[0], coordinates[1])
                    if(mini>distance):
                        mini = distance
                        support_x = a
                        support_y = b
                        label_trans = j
                        #print a,b,x1,y1
                    j= j+1
                if len(label_transition)>0 and label_transition[-1] == label_trans:
                    continue
                label_transition.append(label_trans)
            
            f.write(str(label_start))
            for label in label_transition:
                f.write("\t"+str(label))
            f.write("\n")
            f1.write( str( tup["POLYLINE"][-1][0] ) +"\t" + str( tup["POLYLINE"][-1][1] )+"\n")
            if (tup["DAY_TYPE"]=="A"):
                f2.write(str(label_start))
                for label in label_transition:
                    f2.write("\t"+str(label))
                f2.write("\n")
                f3.write( str( tup["POLYLINE"][-1][0] ) +"\t" + str( tup["POLYLINE"][-1][1] )+"\n")
            else:
                f4.write(str(label_start))
                for label in label_transition:
                    f4.write("\t"+str(label))
                f4.write("\n")
                f5.write( str( tup["POLYLINE"][-1][0] ) +"\t" + str( tup["POLYLINE"][-1][1] )+"\n")    
            
    def train(self):
        f=open("trainC10.txt","w")
        f1=open("trainCA10.txt","w")
        f2=open("trainCD10.txt","w")
        number=0
        for tup in self.mongo_train.find({ '$and':[{'TIME.dayofyear': {'$lt': 333 } }, {'TIME.dayofyear': {'$gte': 273 } },{'DIRTY':0} ]}):
            if len(tup["POLYLINE"]) <22:
                continue
            number+=1
            if number%1000==0:
                print number
                #if number==1000:
                #    break
            mini=10000000
            label_start = -1
            j=0
            for line in self.start:
                a=line[0]
                b=line[1]
                distance=haversine( a, b,tup['POLYLINE'][0][0] ,tup['POLYLINE'][0][1] )
                if(mini>distance):
                    mini = distance
                    support_x = a
                    support_y = b
                    label_start = j
                    #print a,b,x1,y1
                j= j+1
            label_transition=[]
            for coordinates in tup["POLYLINE"][1:-1]:
                mini=10000000
                label_trans = -1
                j=0
                for line in self.trans:
                    
                    #print line[2]
                    a=line[0]
                    
                    b=line[1]
                    distance=haversine( a, b, coordinates[0], coordinates[1])
                    if(mini>distance):
                        mini = distance
                        support_x = a
                        support_y = b
                        label_trans = j
                        #print a,b,x1,y1
                    j= j+1
                if len(label_transition)>0 and label_transition[-1] == label_trans:
                    continue
                label_transition.append(label_trans)
            
            mini=10000000
            label_end = -1
            j=0
            for line in self.end:
                a=line[0]
                b=line[1]
                distance=haversine( a, b,tup['POLYLINE'][-1][0] ,tup['POLYLINE'][-1][1] )
                if(mini>distance):
                    mini = distance
                    support_x = a
                    support_y = b
                    label_end = j
                    #print a,b,x1,y1
                j= j+1
            f.write(str(label_start))
            for label in label_transition:
                f.write("\t"+str(label))
            f.write("\t"+str(label_end)+"\n")
            if (tup["DAY_TYPE"]=="A"):
                f1.write(str(label_start))
                for label in label_transition:
                    f1.write("\t"+str(label))
                f1.write("\t"+str(label_end)+"\n")
            else:
                f2.write(str(label_start))
                for label in label_transition:
                    f2.write("\t"+str(label))
                f2.write("\t"+str(label_end)+"\n")

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
    cot = Creat_test_train()
    cot.train()
    cot.test()
