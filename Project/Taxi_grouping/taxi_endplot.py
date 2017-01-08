import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib

from collections import OrderedDict
from itertools import izip
import pytz
import csv
from matplotlib.legend_handler import HandlerLine2D
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
import json
from math import radians, cos, sin, asin, sqrt, ceil

class Taxi_Plot:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_train = self.mongo_db['calltype_B']
        
    def single_taxistand(self):
        a=[]
        x=[]
        number=0
        c=[]
        for tup in self.mongo_train.find({"ORIGIN_STAND":20}):
            if len(tup["POLYLINE"])<50:
                continue
            a.append([float(tup["POLYLINE"][-1][0]) , float(tup["POLYLINE"][-1][1])] )
            '''
            if self.haversine(float(tup["POLYLINE"][-1][1]) , float(tup["POLYLINE"][-1][0]),float(tup["POLYLINE"][0][1]) , float(tup["POLYLINE"][0][0]))<1000:
                #print tup["POLYLINE"]
                
                x=np.array(tup["POLYLINE"])
                plt.plot(x[0][0],x[0][1],"bo")
                plt.plot(x[1:-2,0],x[1:-2,1],"r")
                plt.plot(x[-1][0],x[-1][1],"go")
                print tup["TRIP_ID"]
                #plt.show()
                break
                '''
            x=[float(tup["POLYLINE"][0][0]) , float(tup["POLYLINE"][0][1])]
            number+=1
            c.append(0)
            if number % 1000==0:
                print number
                if number==10000:
                    break
        a=np.array(a)
        print a
        p,=plt.plot(x[0],x[1],"ro",markersize=12,label='Start Point')
        print x
        q=plt.scatter(a[:, 0], a[:, 1],c=c,marker="^",alpha=0.2,label='Destination')
        plt.legend(handler_map={p:HandlerLine2D(numpoints=1)})
        plt.savefig("Taxi_endplot.png",dpi=1200)
        plt.show()
        
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
    Tp = Taxi_Plot()
    Tp.single_taxistand()
