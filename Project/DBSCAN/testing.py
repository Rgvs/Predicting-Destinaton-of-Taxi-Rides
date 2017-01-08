'''
Created at Jan 31st
Modified Feb 5th
Modified Feb 16th   (added training part)
Modified Feb 23rd
'''
import numpy as np
import re
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
        label_count=-1 
        total_distance = 0 
        new_total_distance= 0
        trips=0
        # matrix creation for training data 
        
        start=[]
        
        end=[]
        f1 = open('db_start.txt' ,'r')
        st=f1.read().split('\n')
        for coordinates in st:
            coordinates=coordinates.split()
            
            try:
                start.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        f1 = open('db_end.txt' ,'r')
        e=f1.read().split('\n')
        for coordinates in e:
            coordinates=coordinates.split()
            try:
                end.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        Matrix = [[0.0 for x in range(0,len(end)+1)] for y in range(0,len(start))]
        

        for line_from_file_1, line_from_file_2 in izip(open('start_fixed.txt'), open('end_fixed.txt')):
            b=int(line_from_file_1.strip())
            c=int(line_from_file_2.strip())
            if( b!= -1 and c != -1):
                #print b
                #print c
                Matrix[b][c] += 1.0
                
        #storing sum for each starting point
        for i in range(0,len(start)):
            add=0.0
            for j in range(0, len(end)):
                add+=Matrix[i][j]
            Matrix[i][len(end)]=add
            
        #changing count to probabilities
        for i in range(0,len(start)-2):
        
            for j in range(0, len(end)):
                try:
                    Matrix[i][j]=Matrix[i][j]/Matrix[i][len(end)]
                except:
                    print Matrix[i][len(end)],i,j
                    #break
                    
        #for tup in self.mongo_train.find({"$and" : [ 
        #                                    { "$or": [ 
        #                                        {'TIME.month':6}, 
        #                                        {'TIME.month':6} 
        #                                        ] } , 
        #                                    {'CALL_TYPE': 'C'}
        #                                    ]}):
        u=g=bad=gg=uu=bb=0
        for tup in self.mongo_train.find({ '$and':[{'TIME.dayofyear': {'$lt': 277 } }, {'TIME.dayofyear': {'$gte': 270 } },{'DIRTY':0} ]}):
            # Generate sample data
            #print "yes"
            number=number+1
            if number%1000==0:
                print number
                if number ==10000:
                    break
            if len(tup["POLYLINE"]) < 20:
                continue
            trips = trips + 1    
            x1= float(tup["POLYLINE"][0][0])
            y1= float(tup["POLYLINE"][0][1])
            #x10 =tup["POLY"][9][0]
            #y10= tup["POLY"][9][1]
            mini=10000000
            label_count = -1
            j=0
            for line in start:
                
                a=line[0]
                b=line[1]
                distance= (a-x1)*(a-x1) + (b-y1)*(b-y1)
                if(mini>distance):
                    mini = distance
                    support_x = a
                    support_y = b
                    label_count = j
                    #print a,b,x1,y1
                j= j+1    
    
            
                        
            #finding destination based on maximum probabilty from matrix
            #label_count=182
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
            if new_distance >  10000:
                trips-=1
                continue         
            #print largest
            #print destination
              
            #verification
            x_last = float(tup["POLYLINE"][-1][0])
            y_last = float(tup["POLYLINE"][-1][1])
            mini=10000000
            label_count = destination
            line = end[label_count]
            #print f1
            a=line[0]
            b=line[1]
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
            total_distance=total_distance + haversine( a, b, x_last, y_last)
            new_total_distance+=new_distance
            print total_distance/trips,gg,bb,uu
            print new_total_distance/trips,g,bad,uu
            
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
