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
        self.mongo_train = self.mongo_db['calltype_B']
        
    def db(self):
        fout  = open("taxi_stand_5","w")
        number=0
        X=[]
        start=[]
        trans=[]
        end=[]
        f1 = open('K_start_CB.txt' ,'r')
        st=f1.read().split('\n')
        for coordinates in st:
            coordinates=coordinates.split()
            try:
                start.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        f1 = open('K_n_transition_K_CB.txt' ,'r')
        t=f1.read().split('\n')
        for coordinates in t:
            coordinates=coordinates.split()
            try:
                trans.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        f1 = open('K_end_CB.txt' ,'r')
        e=f1.read().split('\n')
        for coordinates in e:
            coordinates=coordinates.split()
            try:
                end.append ([ float(coordinates[0]),float(coordinates[1])] )
            except:
                print coordinates
                pass
        label_start=-1 
        total_distance = 0.0 
        trips=0
        total_distance_new = 0.0
        # matrix creation for training data     
        count1=60 #start
        count2=500 #tansition
        count3=250 #destination

        count_good=count_avg=count_bad=0
        Matrix = [[0 for x in range(905)] for x in range(65)]
        max_id = 0 
        min_id = 10000000000000
        for tup in self.mongo_train.find({"$and" :[{"DIRTY" : 0},{"$or": [{"TIME.month":11},{"TIME.month":12}]}] }):
            # Generate sample data
            #print "yes"
            number=number+1
            if number%1000==0:
                print number
            #if number== 10000:
            #    break
            if len(tup["POLYLINE"])/4 < 8:
                continue
            trips = trips + 1
            
            if(tup["TAXI_ID"] >max_id):
                max_id = tup["TAXI_ID"]
            if(tup["TAXI_ID"] < min_id):
                min_id = tup["TAXI_ID"]
            #taxi_matrix[label_start].append(tup["TAXI_ID"])
            
            try:
                Matrix[tup["ORIGIN_STAND"]][int(str(tup["TAXI_ID"])[-3:])] +=1
            except:
                #print int(str(tup["TAXI_ID"])[-3:]), tup["ORIGIN_STAND"],tup["TRIP_ID"]
                pass
        #print min_id , max_id
        #print Matrix
        a=[]
	#fout1  = open("taxi_taxistand_matrix1.txt","w")
        Matrix = np.array(Matrix)
        for i in range(0,905):
            if sum(Matrix[:,i])==1 :
                a.append(i)
        print a
        for i in range(0,65):
            #if(Matrix[:,a[0]][i] == 1):
            print sum(Matrix[i]) , i
        for i in range(0,905):
            if(Matrix[4][i] == 1):
                fout.write(str(20000000 + i)+"\n")
            ###need a new file for transition clusters
	fout2  = open("taxis.txt","w")
	for i in range(0,905):
		flag=0		
		for j in range(0,65):
			if(Matrix[j][i]==1):
				print str(20000000 + i)
				fout2.write(str(20000000 + i)+"\n")				
				break		
			#fout1.write(str(Matrix[j][i]))
			#fout1.write(" ")
		#fout1.write("\n")
if __name__ == '__main__':
    cot = Dbscan()
    cot.db()
