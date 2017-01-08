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
        self.mongo_db = self.mongo_client['Test']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['cleantrainholidays_160_1min']
        self.mongo_test1 = self.mongo_db['cleantrainholidays_160_1min_daytype_A']
        self.mongo_test2 = self.mongo_db['cleantrainholidays_160_1min_daytype_B']
        self.mongo_test3 = self.mongo_db['cleantrainholidays_160_1min_daytype_C']
        self.mongo_test4 = self.mongo_db['cleantrainholidays_160_1min_daytype_D']

    def convert(self):
    	number  = 0
        for tup in self.mongo_train.find():
            new_gps=[]
            number = number + 1
            if number % 1000 == 0:
                print(number)
            try:
                #new_gps.append([tup["POLY"][0][0],tup["POLY"][0][1],1])
                for count in range(0,len(tup["POLY"])-1):
                    
                    if (tup["DAY_TYPE"] == "A"):
                       self.mongo_test1.insert(tup) 
                    if (tup["DAY_TYPE"] == "B"):
                       self.mongo_test2.insert(tup) 
                    if (tup["DAY_TYPE"] == "C"):
                       self.mongo_test3.insert(tup) 
                    if (tup["DAY_TYPE"] == "D"):
                       self.mongo_test4.insert(tup) 
                    
                
            except:
                pass

    


           
if __name__ == '__main__':
    cot = Convert()
    cot.convert()
