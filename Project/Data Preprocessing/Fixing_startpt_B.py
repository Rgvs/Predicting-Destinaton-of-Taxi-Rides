'''
Created at April 16th
'''
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
import json
from math import radians, cos, sin, asin, sqrt, ceil
class Fix:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_train = self.mongo_db['cleantrain_160mts']
        #self.mongo_test = self.mongo_db['cleantraintruncation_160mts']
        metadata=open("metaData_taxistand.csv","r")
        self.taxi=[]
        line=metadata.readline()
        for line in metadata:
            line =line.split(",")
            self.taxi.append( [ float (line[2]), float(line[3][:-1]) ] )
    
    def start_point(self):
        number  = 0
        #print taxi
        count1=0
        for tup in self.mongo_train.find({"CALL_TYPE":"B"}):
            new_gps=[]
            number = number + 1
            if number % 5000 == 0:
                print(number)
                print count1
            try:
                new_gps.append([self.taxi[tup["ORIGIN_STAND"]-1][1],self.taxi[tup["ORIGIN_STAND"]-1][0],1])
                for count in range(0,len(tup["POLYLINE"])):
                    a=tup["POLYLINE"][count][0]
                    b=tup["POLYLINE"][count][1]
                    c=tup["POLYLINE"][count][2]
                    #print a,b,c
                    new_gps.append([float(a),float(b),c])
                tup["POLYLINE"]=new_gps
                #print new_gps[0][1],new_gps[0][0],new_gps[1][1],new_gps[1][0]
                #if tup["ORIGIN_STAND"]==62:
                if self.haversine (new_gps[0][1],new_gps[0][0],new_gps[1][1],new_gps[1][0])>1000:
                    self.mongo_train.remove({"_id":tup["_id"]})
                    count1+=1
                    continue
                #print tup["POLY"]        
                self.mongo_train.update_one({"_id":tup["_id"]},{'$set':{'POLYLINE':tup['POLYLINE'] }})
            except:
                pass
    def origin_stand(self):
        number=0
        for tup in self.mongo_train.find({"$and":[{"CALL_TYPE":"B"},{"ORIGIN_STAND":""}]}):
            number+=1
            print number
            minimum=100000
            for i in range(0,len(self.taxi)):
                if len(tup["POLYLINE"])>0 and minimum> self.haversine(self.taxi[i][0],self.taxi[i][1],tup["POLYLINE"][0][1],tup["POLYLINE"][0][0]):
                    minimum =self.haversine(self.taxi[i][0],self.taxi[i][1],tup["POLYLINE"][0][1],tup["POLYLINE"][0][0])
                    tup["ORIGIN_STAND"]=i+1
            if minimum<=1000:
                self.mongo_train.update_one({"_id":tup["_id"]},{'$set':{'ORIGIN_STAND':tup['ORIGIN_STAND'] }})
            else:
                self.mongo_train.remove({"_id":tup["_id"]})
    def haversine(self,lon1, lat1, lon2, lat2):
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
    cot = Fix()
    #cot.start_point()
    cot.origin_stand()
