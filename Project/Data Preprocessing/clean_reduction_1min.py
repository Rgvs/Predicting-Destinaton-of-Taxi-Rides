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
        self.mongo_train = self.mongo_db['cleantrain_160']
        #self.mongo_test1min=self.mongo_db['cleantrain_160_1min']
        self.mongo_trainH = self.mongo_db['cleantrainholidays_160_1min']
        self.mongo_testA = self.mongo_db['cleantrainholidays_160_1min_daytype_A']
        self.mongo_testB = self.mongo_db['cleantrainholidays_160_1min_daytype_B']
        self.mongo_testC = self.mongo_db['cleantrainholidays_160_1min_daytype_C']
        self.mongo_testD = self.mongo_db['cleantrainholidays_160_1min_daytype_D']  

    def convert(self):
    	number  = 0
    	holidays=[[15,8,2013] ,[8,12,2013] ,[25,12,2013] ,[1,1,2014] ,[18,4,2014] ,[20,4,2014] ,[25,4,2014] ,[1,5,2014] ,[10,6,2014],[15,8,2014],[8,12,2014],[25,12,2014]]
        preholidays=[[14,8,2013] ,[7,12,2013] ,[24,12,2013] ,[31,12,2013] ,[17,4,2014] ,[19,4,2014] ,[24,4,2014] ,[30,4,2014] ,[9,6,2014],[14,8,2014],[7,12,2014],[24,12,2014]]
        for tup in self.mongo_train.find():
            new_gps=[]
            number = number + 1
            if number % 1000 == 0:
                print(number)
            if number==1:
                min_lat = tup["POLY"][0][0]
                max_lat = tup["POLY"][0][0]
                min_long = tup["POLY"][0][1]
                max_long = tup["POLY"][0][1] 
            try:
                for count in range(0,len(tup["POLY"])-1):
                    if(tup["POLY"][count][0] < min_lat) :
                        min_lat = tup["POLY"][count][0]
                        print min_lat,"min_lat"
                    elif(tup["POLY"][count][0] > max_lat) :
                        max_lat = tup["POLY"][count][0]
                        print max_lat,"max_lat"
                    if(tup["POLY"][count][1] < min_long) :
                        min_long = tup["POLY"][count][1]
                        print min_long,"min_long"
                    elif(tup["POLY"][count][1] > max_long) :
                        max_long = tup["POLY"][count][1] 
                        print max_long,"max_long" 
                    if(count%4==0):
                        new_gps.append(tup["POLY"][count])
                tup["POLY"] = new_gps
                #print "ok"
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
                
                
                #new_gps.append([tup["POLY"][0][0],tup["POLY"][0][1],1])
                    
                self.mongo_trainH.insert(tup)
                if (tup["DAY_TYPE"] == "A"):
                   self.mongo_testA.insert(tup) 
                elif (tup["DAY_TYPE"] == "B"):
                   self.mongo_testB.insert(tup) 
                elif (tup["DAY_TYPE"] == "C"):
                   self.mongo_testC.insert(tup) 
                elif (tup["DAY_TYPE"] == "D"):
                   self.mongo_testD.insert(tup) 
                
            except:
                print "NO"
                pass
        print(max_lat)
        print min_lat
        print(min_long)
        print(max_long)  
if __name__ == '__main__':
    cot = Convert()
    cot.convert()
