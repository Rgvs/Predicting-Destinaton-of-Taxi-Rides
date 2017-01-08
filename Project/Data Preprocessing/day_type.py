'''
Created at Nov 4th
'''
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
import json
from math import radians, cos, sin, asin, sqrt, ceil

class Day_Type:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['Test']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['cleantrain_160_1min']
        self.mongo_test1=self.mongo_db['cleantrainholidays_160_1min']
        
    def convert(self):
        number = 0
        holidays=[[15,8,2013] ,[8,12,2013] ,[25,12,2013] ,[1,1,2014] ,[18,4,2014] ,[20,4,2014] ,[25,4,2014] ,[1,5,2014] ,[10,6,2014],[15,8,2014],[8,12,2014],[25,12,2014]]
        preholidays=[[14,8,2013] ,[7,12,2013] ,[24,12,2013] ,[31,12,2013] ,[17,4,2014] ,[19,4,2014] ,[24,4,2014] ,[30,4,2014] ,[9,6,2014],[14,8,2014],[7,12,2014],[24,12,2014]]
        for tup in self.mongo_train.find():
            number = number + 1
            if number % 1000 == 0:
                print(number)
            if tup["Time"]["weekday"]==6 or tup["Time"]["weekday"]==7 :
                 tup["DAY_TYPE"]="D"
            for date in holidays:
                check_date=tup["Time"]
                if (check_date["dayofmonth"]==date[0] and check_date["month"]==date[1] and check_date["year"]==date[2]):
                     tup["DAY_TYPE"]="C"
            for date in preholidays:
                check_date=tup["Time"]
                if (check_date["dayofmonth"]==date[0] and check_date["month"]==date[1] and check_date["year"]==date[2]):
                     tup["DAY_TYPE"]="B"
            self.mongo_test1.insert(tup)
    

           
if __name__ == '__main__':
    cot = Day_Type()
    cot.convert()
