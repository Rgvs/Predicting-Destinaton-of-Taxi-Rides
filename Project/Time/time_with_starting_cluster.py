'''
Created at Apr 12th
'''
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
import json
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt, ceil
class Convert:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['calltype_A']
        self.mongo_test1=self.mongo_db['test_stn']
        
    def time_segregation_with_starting_coordinate(self):
        time_array = [[0 for x in range(250)] for x in range(24)]	#300 starting clusters(coloumns) and 24 hours(rows)
        number = 0
        for tup in self.mongo_train.find({"$or":[{'TIME.month':7},{'TIME.month':8}]}):
            number +=1
            if(number >=50000):
                break
            hour = tup['TIME']['hour']
            minute = tup['TIME']['min']
            if(len (tup['POLYLINE']) == 0):
                continue
            x_t = float(tup['POLYLINE'][0][0])
            y_t = float(tup['POLYLINE'][0][1])
            #print x_t,y_t
            smallest_distance = 1000000000
            start_cluster = open('K_start_Kaggle_CA.txt','r')
            count = -1
            flag = 0
            for line in start_cluster:
                count +=1
                line = line.split()
                a = float(line[0])
                b = float(line[1])
                distance = haversine(x_t ,y_t , a , b)
                #print distance
                if distance < smallest_distance :
                    smallest_distance = distance
                    flag = count
                    
            #print hour,count        
            time_array[hour][flag] +=1
            
            
            #print time_array
            
        #print time_array,number
        for i in range(0,24):
            for  j in range (0,250):
                print time_array[i][j],
                
            print "\n"
            #time_array[hour]+=1
            
'''
        print time_array
        N = len(time_array)
        x= range(N)
        width =1/1.5
        plt.bar(x,time_array,width,color = "blue")
        plt.savefig("time_segregation.png",dpi = 1000)
        plt.show()
'''

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
    cot = Convert()
    cot.time_segregation_with_starting_coordinate()
