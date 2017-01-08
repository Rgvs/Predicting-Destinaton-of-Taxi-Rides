'''
Created at FEB 4th
Modifeid on April 17th
'''
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
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
        self.mongo_train = self.mongo_db['cleantrain_160mts']
        self.mongo_test = self.mongo_db['cleantraintruncation_final']
        
    def convert(self):
        pre=[0.0,0.0]
        nex=[0.0,0.0]
        flag=0
        flagged=0
        number=0
        count=0
        for tup in self.mongo_test.find({"DIRTY":0}):
            
            
            x=np.array(tup["POLYLINE"])
            if len(x)<50 or self.haversine(x[0][0],x[0][1],x[-1][0],x[-1][1])>250:
                continue
            print self.haversine(x[0][0],x[0][1],x[-1][0],x[-1][1])
            number+=1
            plt.plot(x[:,0],x[:,1],"b")
            l=[]
            m=[]
            for a in x:
                #print a
                if a[2]==1.0:
                    l.append(a[0])
                    m.append(a[1])
            p,=plt.plot(l,m,"bo",label='Transition point')
            q,=plt.plot(x[0][0],x[0][1],"ro",markersize=14,label='Start point')
            r,=plt.plot(x[-1][0],x[-1][1],"go",markersize=14,label='Destination')
            print tup["TRIP_ID"]
            plt.legend(handler_map={p:HandlerLine2D(numpoints=1),q:HandlerLine2D(numpoints=1),r:HandlerLine2D(numpoints=1)})
            plt.savefig(str(100+number)+".png",dpi = 1200)
            plt.show()
            
            if number == 30:
                break
    '''
            for a in tup['POLYLINE']:
                print a
                if a[2]==1 and flag==0:
                    pre=[float(a[0]),float(a[1])]
                    flag=1
                if a[2]==1 and flag==1:
                    nex=[float(a[0]),float(a[1])]
                    #print pre,nex
                    distance= self.haversine(pre[1],pre[0],nex[1],nex[0])
                    print distance
                    if distance > 1000:
                        count+=1
                        print number,distance,count,pre,nex,tup["_id"]
                        #self.mongo_train.remove({"_id":tup["_id"]})
                        flagged=1
                        x=np.array(tup["POLYLINE"])
                        plt.plot(x[0][0],x[0][1],"ro")
                        plt.plot(x[:,0],x[:,1],"b")
                        plt.plot(x[-1][0],x[-1][1],"go")
                        print tup["TRIP_ID"]
                        plt.show()
                        break
                    else:
                        pre=nex
                        
            if flagged==1 or len(tup["POLYLINE"])<15:
                flagged=0
                continue
            new_gps=[]
            number = number + 1
            if number % 5000 == 0:
                print(number)
            try:
                #new_gps.append([tup["POLY"][0][0],tup["POLY"][0][1],1])
                for i in range(0,len(tup["POLYLINE"])):
                    a="%.4f" % tup["POLYLINE"][i][0]
                    b="%.4f" % tup["POLYLINE"][i][1]
                    c=tup["POLYLINE"][i][2]
                    #print a,b,c
                    new_gps.append([a,b,c])
                tup["POLYLINE"]=new_gps
                #print tup["POLY"]        
                #self.mongo_test.insert(tup)
            except:
                pass
             '''
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
