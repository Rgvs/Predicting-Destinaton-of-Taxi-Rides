'''
Created at Feb 5th
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
        self.mongo_test = self.mongo_db['cthrvt_160_1min']
        self.mongo_train = self.mongo_db['cthrvt_160_6min']
        
    def convert(self):
    	number  = 0
    	for tup in self.mongo_test.find():
            new_gps=[]
            number = number + 1
            poly_count=0            
            if number % 1000 == 0:
                print(number)
            try:
                for count in range(0,len(tup["POLY"])-1):
                    if(count%6==0):
                        new_gps.append(tup["POLY"][count])
                        poly_count=poly_count+1
                if (len(tup["POLY"]) %6 != 1):
                    new_gps.append(tup["POLY"][-1])
                    poly_count=poly_count+1
                tup["POLY"] = new_gps
                tup["POLYLINE"]=poly_count
                self.mongo_train.insert(tup)
            except:
                print "NO"
                pass
          
if __name__ == '__main__':
    cot = Convert()
    cot.convert()
