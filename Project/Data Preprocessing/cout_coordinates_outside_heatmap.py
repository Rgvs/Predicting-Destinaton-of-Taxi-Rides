'''
Created at Nov 4th
'''
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
import json
from math import radians, cos, sin, asin, sqrt, ceil
class Convert:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_train = self.mongo_db['cleantraintruncation_160mts']
        #self.mongo_test1=self.mongo_db['cleanedtrain_160_1min']  

    def convert(self):
        number  = 0
        min_lat = 41.04961
        max_lat = 41.24961
        min_long = -8.71099
        max_long = -8.51099
        res=0
        temp=res
        cnt = 0
        for tup in self.mongo_train.find():
            #new_gps=[]
            number = number + 1
            if number % 10000 == 0:
                print(number)
            try:
                #new_gps.append([tup["POLY"][0][0],tup["POLY"][0][1],1])
                for count in range(0,len(tup["POLYLINE"])-1):
                    if(float(tup["POLYLINE"][count][0])> max_long or float(tup["POLYLINE"][count][0])< min_long or float(tup["POLYLINE"][count][1]) > max_lat or float(tup["POLYLINE"][count][1]) < min_lat):
                        print tup["POLYLINE"][count],res,number
                        self.mongo_train.remove({"_id":tup["_id"]})
                        res=res+1
                        break
            except:
                pass
        print (res)
if __name__ == '__main__':
    cot = Convert()
    cot.convert()
