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
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['cleantrain_160mts']
        #self.mongo_test1=self.mongo_db['cleanedtrain']
    def convert(self):
        number  = 0
        count1 =0
        for tup in self.mongo_train.find():
            #new_gps=[]
            number = number + 1
            if number % 1000 == 0:
                print(number)
            count1+=len(tup["POLYLINE"])
            #try:
            #    new_gps.append([tup["POLY"][0][0],tup["POLY"][0][1],1])
                #for count in range(0,len(tup["POLY"])-1):
                #    count1 = count1 + 1
            '''
                    pre=tup["POLY"][count]
                    nex=tup["POLY"][count+1]
                    for coordinate in list
                        x.append([a[count],b[count]])
                    self.mongo_ex.insert x
                        
                    distance= self.haversine(pre[1],pre[0],nex[1],nex[0])
                    if distance > 100 :
                        k= ceil(distance/100) - 1
                        for x in range(1,int(k)+1):
                            x=x+0.0
                            new_gps.append([pre[0]+(pre[0]-nex[0])*x/(k+1),pre[1]+(pre[1]-nex[1])*x/(k+1),0]) #lat ,long, added
                            #print (pre[0]-nex[0])*x/(k+1),pre[0],nex[0],x,k
                    new_gps.append([nex[0],nex[1],1]) #lat,long,original
                tup["POLY"] = new_gps
                #print new_gps
                self.mongo_test1.insert(tup)
            '''
            #except:
            #    pass
        print(count1)
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
    cot = Convert()
    cot.convert()
