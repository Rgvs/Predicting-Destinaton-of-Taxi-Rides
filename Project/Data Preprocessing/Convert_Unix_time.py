'''
Created at Nov 4th
Excuted 29 Jan
'''
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
import json
class Convert:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['cleantrain_160mts']
        self.mongo_test=self.mongo_db['test_stn']
        
    def convert(self):
        number=0
        for tup in self.mongo_train.find():
            #print tup['TIMESTAMP']
            number+=1
            if number%1000==0:
                print number
            dt=datetime.datetime.utcfromtimestamp(tup['TIMESTAMP'])
            #localtz = pytz.timezone('GMT')
            #dt = localtz.localize(dt)
            #print dt
            #print dt.weekday()
            tup['TIME']={}
            tup['TIME']['weekday']=dt.isoweekday()
            tup['TIME']['dayofmonth']=dt.day
            tup['TIME']['month']=dt.month
            tup['TIME']['year']=dt.year
            tup['TIME']['hour']=dt.hour
            tup['TIME']['min']=dt.minute
            tup['TIME']['sec']=dt.second
            tup['TIME']['dayofyear']=int(dt.strftime('%j'))
            #print tup['POLYLINE']
            self.mongo_train.update_one({"_id":tup["_id"]},{'$set':{'TIME':tup['TIME'] }})
           
if __name__ == '__main__':
    cot = Convert()
    cot.convert()
