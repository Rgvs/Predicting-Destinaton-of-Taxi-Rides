'''
Created at March 14
'''
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
import json
from math import radians, cos, sin, asin, sqrt, ceil
class Seg:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['cleantraintruncation_160mts']
        self.mongo_test1 = self.mongo_db['160_daytype_A']
        self.mongo_test2 = self.mongo_db['160_daytype_B']
        self.mongo_test3 = self.mongo_db['160_daytype_C']
        self.mongo_test4 = self.mongo_db['160_daytype_D']
        self.mongo_test5 = self.mongo_db['160_calltype_A']
        self.mongo_test6 = self.mongo_db['160_calltype_B']
        self.mongo_test7 = self.mongo_db['160_calltype_C']
        #self.mongo_test4 = self.mongo_db['160_daytype_D']

    def segg(self):
    	number  = 0
        for tup in self.mongo_train.find():
            number = number + 1
            if number % 1000 == 0:
                print(number)
            try:
                if (tup["DAY_TYPE"] == "A"):
                   self.mongo_test1.insert(tup) 
                elif (tup["DAY_TYPE"] == "B"):
                   self.mongo_test2.insert(tup) 
                elif (tup["DAY_TYPE"] == "C"):
                   self.mongo_test3.insert(tup) 
                elif (tup["DAY_TYPE"] == "D"):
                   self.mongo_test4.insert(tup) 
            
                if (tup["CALL_TYPE"] == "A"):
                   self.mongo_test5.insert(tup) 
                elif (tup["CALL_TYPE"] == "B"):
                   self.mongo_test6.insert(tup) 
                elif (tup["CALL_TYPE"] == "C"):
                   self.mongo_test7.insert(tup) 
            except:
                print "Fail"
                pass

if __name__ == '__main__':
    s = Seg()
    s.segg()
