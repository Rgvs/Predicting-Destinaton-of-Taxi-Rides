'''
Created at April 14th
'''
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
import json
from math import radians, cos, sin, asin, sqrt, ceil

class Clean:

    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_train = self.mongo_db['cleantraintruncation_160mts']
    
    def mainclean(self):
        pre=[0.0,0.0]
        nex=[0.0,0.0]
        flag=0
        number=0
        count=0
        for tup in self.mongo_train.find():
            flag=0
            count+=1
            for a in tup['POLYLINE']:
                if a[2]==0 and flag==0:
                    pre=[float(a[0]),float(a[1])]
                    flag=1
                if a[2]==0 and flag==1:
                    nex=[float(a[0]),float(a[1])]
                    #print pre,nex
                    distance= self.haversine(pre[1],pre[0],nex[1],nex[0])
                    if distance > 1000:
                        number+=1
                        print number,distance,count,pre,nex,tup["_id"]
                        self.mongo_train.remove({"_id":tup["_id"]})
                        break
                    else:
                        pre=nex

            
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
    cot = Clean()
    cot.mainclean()
