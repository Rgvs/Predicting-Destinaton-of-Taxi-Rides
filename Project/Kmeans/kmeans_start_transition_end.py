'''
Created at Jan 31st
Modified Feb 5th
Modified Feb 16th   (added training part)
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
        self.mongo_train = self.mongo_db['cthrvt_160_1min']
        
    def db(self):
        
        number=0
        X=[]
        label_count=-1 
        total_distance = 0 
        trips=0
        for tup in self.mongo_train.find({"$or":[{'Time.month':10}, {'Time.month':11}]}):
            # Generate sample data
            #print "yes"
            number=number+1
            if number%1000==0:
                print number
            #if number== 10000:
            #    break
            if len(tup["POLY"]) < 30:
                continue
            trips = trips + 1    
            x1= float(tup["POLY"][0][0])
            y1= float(tup["POLY"][0][1])
            x5= float(tup["POLY"][5][0])
            y5= float(tup["POLY"][5][1])
            
            #x10 =tup["POLY"][9][0]
            #y10= tup["POLY"][9][1]
            f1 = open('Start' ,'r')
            mini=10000000
            label_count = -1
            j=0
            for line in f1:
                line=line.split()
                a=float(line[0][1:-1])
                b=float(line[1][:-1])
                distance=haversine( a, b, x1, y1)
                if(mini>distance):
                    mini = distance
                    support_x = a
                    support_y = b
                    label_count = j
                    #print a,b,x1,y1
                j= j+1    
    
            # matrix creation for training data 	
            count1=150
            #for line_from_file_1 in izip(open('Start')):
            #    count1=count1+1
            #print count1
            count2=150
            #for line_from_file_1 in izip(open('End.txt')):
            #    count2=count2+1
            #print count2

            Matrix = [[0.0 for x in range(0,count2+1)] for y in range(0,count1)]

            for line in izip(open('start_transition_end_K.txt')):
                
                b=int(line)
                print b
                exit(0)
                if( b!= -1 and c != -1):
                    #print b
                    #print c
                    Matrix[b][c] += 1.0
                    
            #storing sum for each starting point
            for i in range(0,count1):
                add=0.0
                for j in range(0, count2):
                    add+=Matrix[i][j]
                Matrix[i][count2]=add
                
            #changing count to probabilities
            for i in range(0,count1):
                for j in range(0, count2):
                    Matrix[i][j]=Matrix[i][j]/Matrix[i][count2]
            '''        
            for i in range(0,count1-1):
                for j in range(0,count2-1):
                    print Matrix[i][j],
                print '\n'
            '''
                
            #finding destination based on maximum probabilty from matrix
            #label_count=182
            
            
            
            largest=-1.5
            destination=0
            #print label_count
            for j in range(0, count2):
                if(largest < Matrix[label_count][j]):
                    #print Matrix[label_count][j]
                    #print type(j)
                    destination=int(j)
                    largest = Matrix[label_count][j]
                    
                    
            #print largest
            #print destination
              
            #verification
            '''
            x_last = float(tup["POLY"][-1][0])
            y_last = float(tup["POLY"][-1][1])
            f1 = open('End.txt' ,'r')
            mini=10000000
            label_count = destination
            f1 = f1.read().split('\n')[label_count]
            #print f1
            line=f1.split()
            a=float(line[0][1:-1])
            b=float(line[1][:-1])
            total_distance=total_distance + haversine( a, b, x_last, y_last)
            #print total_distance/trips
            '''
            
            
            #finding 5 closest destinations to transition points
            
            d=[0.0,0.0,0.0,0.0,0.0]
            e=[-1,-1,-1,-1,-1]
            for j in range(0,5):
                #f2 = open('End.txt' ,'r')
                #f2 = f2.read().split('\n')[j]
                #line=f2.split()
                #a=float(line[0][1:-1])
                #b=float(line[1][:-1])
                #d[j]=haversine( a, b, x5, y5)
                #e[j]=j
                #print label_count, j
                d[j]=Matrix[label_count][j]
                e[j]=j
                
            
            
             
            for j in range(5,count2):
                #f3 = open('End.txt' ,'r')  
                val, idx = min((val, idx) for (idx, val) in enumerate(d))
                #f3= f3.read().split('\n')[j]
                #line=f3.split()
                #a=float(line[0][1:-1])
                #b=float(line[1][:-1])
                #dist=haversine( a, b, x5, y5)
                if Matrix[label_count][j]>val:
                    d[idx]=Matrix[label_count][j]
                    e[idx]=j
            dist=0
            least=1000000000.0
            last_x=0.0
            last_y=0.0 
            for j in range(0,5):
                #print d[j], Matrix[label_count][e[j]]
                if(d[j]!=0):
                    f3 = open('End.txt' ,'r')
                    f3= f3.read().split('\n')[e[j]]
                    line=f3.split()
                    a=float(line[0][1:-1])
                    b=float(line[1][:-1])
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
            f1 = open('End.txt' ,'r')
            mini=10000000
            f1 = f1.read().split('\n')[label_end]
            #print f1
            line=f1.split()
            a=float(line[0][1:-1])
            b=float(line[1][:-1])
            total_distance=total_distance + haversine( a, b, x_last, y_last)
            if trips%1000==0:
                print total_distance/trips
                
            
                
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
