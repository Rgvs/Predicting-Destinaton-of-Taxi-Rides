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
        self.mongo_train = self.mongo_db['cleantraintruncation1kmremoval_15*160mts']
        self.mongo_test1 = self.mongo_db['daytype_A_calltype_A']
        self.mongo_test2 = self.mongo_db['daytype_A_calltype_B']
        self.mongo_test3 = self.mongo_db['daytype_A_calltype_C']
        self.mongo_test4 = self.mongo_db['daytype_B_calltype_A']
        self.mongo_test5 = self.mongo_db['daytype_B_calltype_B']
        self.mongo_test6 = self.mongo_db['daytype_B_calltype_C']
        self.mongo_test7 = self.mongo_db['daytype_C_calltype_A']
        self.mongo_test8 = self.mongo_db['daytype_C_calltype_B']
        self.mongo_test9 = self.mongo_db['daytype_C_calltype_C']
        self.mongo_test10 = self.mongo_db['daytype_D_calltype_A']
        self.mongo_test11 = self.mongo_db['daytype_D_calltype_B']
        self.mongo_test12 = self.mongo_db['daytype_D_calltype_C']
        self.mongo_test13 = self.mongo_db['daytype_A']
        self.mongo_test14 = self.mongo_db['daytype_B']
        self.mongo_test15 = self.mongo_db['daytype_C']
        self.mongo_test16 = self.mongo_db['daytype_D']
        self.mongo_test17 = self.mongo_db['calltype_A']
        self.mongo_test18 = self.mongo_db['calltype_B']
        self.mongo_test19 = self.mongo_db['calltype_C']

    def segg(self):
    	number  = 0
        for tup in self.mongo_train.find():
            number = number + 1
            if number % 1000 == 0:
                print(number)
            try:
                if (tup["DAY_TYPE"] == "A"):
                   self.mongo_test13.insert(tup)
                elif (tup["DAY_TYPE"] == "B"):
                   self.mongo_test14.insert(tup) 
                elif (tup["DAY_TYPE"] == "C"):
                   self.mongo_test15.insert(tup) 
                elif (tup["DAY_TYPE"] == "D"):
                   self.mongo_test16.insert(tup)                  
                if (tup["CALL_TYPE"] == "A"):
                   self.mongo_test17.insert(tup) 
                elif (tup["CALL_TYPE"] == "B"):
                   self.mongo_test18.insert(tup) 
                elif (tup["CALL_TYPE"] == "C"):
                   self.mongo_test19.insert(tup) 
                if (tup["DAY_TYPE"] == "A" and tup["CALL_TYPE"] == "A"):
                   self.mongo_test1.insert(tup) 
                elif (tup["DAY_TYPE"] == "A" and tup["CALL_TYPE"] == "B"):
                   self.mongo_test2.insert(tup) 
                elif (tup["DAY_TYPE"] == "A" and tup["CALL_TYPE"] == "C"):
                   self.mongo_test3.insert(tup) 
                elif (tup["DAY_TYPE"] == "B" and tup["CALL_TYPE"] == "A"):
                   self.mongo_test4.insert(tup)
                elif (tup["DAY_TYPE"] == "B" and tup["CALL_TYPE"] == "B"):
                   self.mongo_test5.insert(tup)
                elif (tup["DAY_TYPE"] == "B" and tup["CALL_TYPE"] == "C"):
                   self.mongo_test6.insert(tup)
                elif (tup["DAY_TYPE"] == "C" and tup["CALL_TYPE"] == "A"):
                   self.mongo_test7.insert(tup)
                elif (tup["DAY_TYPE"] == "C" and tup["CALL_TYPE"] == "B"):
                   self.mongo_test8.insert(tup)
                elif (tup["DAY_TYPE"] == "C" and tup["CALL_TYPE"] == "C"):
                   self.mongo_test9.insert(tup)
                elif (tup["DAY_TYPE"] == "D" and tup["CALL_TYPE"] == "A"):
                   self.mongo_test10.insert(tup) 
                elif (tup["DAY_TYPE"] == "D" and tup["CALL_TYPE"] == "B"):
                   self.mongo_test11.insert(tup)
                elif (tup["DAY_TYPE"] == "D" and tup["CALL_TYPE"] == "C"):
                   self.mongo_test12.insert(tup)       
               
            
            except:
                print "Fail"
                pass

if __name__ == '__main__':
    s = Seg()
    s.segg()
