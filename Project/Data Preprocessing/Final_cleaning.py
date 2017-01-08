'''
Created at Feb 29th
Modified on april 22nd
'''
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
import json
from math import radians, cos, sin, asin, sqrt, ceil
holidays=[[15,8,2013], [8,12,2013], [25,12,2013], [1,1,2014], [18,4,2014], [20,4,2014], [25,4,2014], [1,5,2014], [10,6,2014], [15,8,2014], [8,12,2014], [25,12,2014]]
preholidays=[[14,8,2013] ,[7,12,2013] ,[24,12,2013] ,[31,12,2013] ,[17,4,2014] ,[19,4,2014] ,[24,4,2014] ,[30,4,2014] ,[9,6,2014],[14,8,2014],[7,12,2014],[24,12,2014]]
class Clean:

    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_train = self.mongo_db['train']
        self.mongo_trainH = self.mongo_db['cleantraintruncation_final']
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
        metadata=open("metaData_taxistand.csv","r")
        self.taxi=[]
        line=metadata.readline()
        for line in metadata:
            line =line.split(",")
            self.taxi.append( [ float (line[2]), float(line[3][:-1]) ] )
            
    def mainclean(self):
        number=0
        self.out=0
        self.mongo_trainH.drop()
        self.mongo_test1.drop()
        self.mongo_test2.drop()
        self.mongo_test3.drop()
        self.mongo_test4.drop()
        self.mongo_test5.drop()
        self.mongo_test6.drop()
        self.mongo_test7.drop()
        self.mongo_test8.drop()
        self.mongo_test9.drop()
        self.mongo_test10.drop()
        self.mongo_test11.drop()
        self.mongo_test12.drop()
        self.mongo_test13.drop()
        self.mongo_test14.drop()
        self.mongo_test15.drop()
        self.mongo_test16.drop()
        self.mongo_test17.drop()
        self.mongo_test18.drop()
        self.mongo_test19.drop()
        for tup in self.mongo_train.find():
            #print tup
            tup['DIRTY']=0
            tup['TIME']=self.timefix(tup['TIMESTAMP'])
            #print tup["POLYLINE"]
            tup['POLYLINE']=self.polyfix(tup['POLYLINE'])
            #print tup["POLYLINE"]
            tup['DAY_TYPE']=self.dayfix(tup['TIME'])
            tup=self.clean(tup)
            tup['POLYLINE']=self.truncation(tup['POLYLINE'])
            #print tup["POLYLINE"]
            if tup['CALL_TYPE'] =='B':
                tup=self.start_point(tup)
            if tup['CALL_TYPE'] =='B' and tup['ORIGIN_STAND']=='':
                tup['ORIGIN_STAND']=self.origin_stand(tup)
                if tup['ORIGIN_STAND']==-1:
                    tup['DIRTY']=1
            if number%1000 == 0:
                print number,self.out
                #if number == 10000:
                #    break
            self.segg(tup)
            number+=1
            #break
            self.mongo_trainH.insert(tup)
    def start_point(self,tup):
        new_gps=[]
        try:
            new_gps.append([self.taxi[tup["ORIGIN_STAND"]-1][1],self.taxi[tup["ORIGIN_STAND"]-1][0],1])
            for count in range(0,len(tup["POLYLINE"])):
                a=tup["POLYLINE"][count][0]
                b=tup["POLYLINE"][count][1]
                c=tup["POLYLINE"][count][2]
                #print a,b,c
                new_gps.append([float(a),float(b),c])
            tup["POLYLINE"]=new_gps
            if self.haversine (new_gps[0][0],new_gps[0][1],new_gps[1][0],new_gps[1][1])>1000:
                tup['DIRTY']=1
        except:
            pass
        return tup
        
    def origin_stand(self,tup):
        minimum=100000
        #print tup["POLYLINE"][0][1],tup["POLYLINE"][0][0]
        for i in range(0,len(self.taxi)):
            if len(tup["POLYLINE"])>0  and minimum> self.haversine(self.taxi[i][1],self.taxi[i][0],tup["POLYLINE"][0][0],tup["POLYLINE"][0][1]):
                minimum =self.haversine(self.taxi[i][1],self.taxi[i][0],tup["POLYLINE"][0][0],tup["POLYLINE"][0][1])
                tup["ORIGIN_STAND"]=i+1
        if minimum<=1000:
            return tup["ORIGIN_STAND"]
        else:
            return -1
            
    def truncation(self,polyline):
        new_gps=[]
        for i in range(0,len(polyline)):
            try:
                a="%.4f" % polyline[i][0]
                b="%.4f" % polyline[i][1]
                c=polyline[i][2]
                #print a,b,c
                new_gps.append([float(a),float(b),c])
            except:
                print polyline,len(polyline)
                break
        return new_gps
        
    def timefix(self,timestamp):
        dt=datetime.datetime.utcfromtimestamp(timestamp)
        #localtz = pytz.timezone('GMT')
        #dt = localtz.localize(dt)
        tup={}
        tup['weekday']=dt.isoweekday()
        tup['dayofmonth']=dt.day
        tup['month']=dt.month
        tup['year']=dt.year
        tup['hour']=dt.hour
        tup['min']=dt.minute
        tup['sec']=dt.second
        tup['dayofyear']=int(dt.strftime('%j'))
        return tup
        #print tup['POLYLINE']
        
    def polyfix(self,polyline):
        tup=(polyline[1:-1]).split("],[")
        fix_tup=[]
        tup[0]=tup[0][1:]
        tup[-1]=tup[-1][:-1]
        if len(polyline)==2:
            return []
        for pair in tup:
            y=(pair.split(","))
            #print y
            y[0]=float(y[0])
            y[1]=float(y[1])
            #print y
            fix_tup.append(y)
        #print tup["POLY"]
        return fix_tup
    
    def dayfix(self,time):
        for date in holidays:
            check_date=time
            if (check_date["dayofmonth"]==date[0] and check_date["month"]==date[1] and check_date["year"]==date[2]):
                 return "C"
        for date in preholidays:
            check_date=time
            if (check_date["dayofmonth"]==date[0] and check_date["month"]==date[1] and check_date["year"]==date[2]):
                 return "B"
        if time["weekday"]==6 or time["weekday"]==7 :
            return "D"
        return "A"
    
    def clean(self,tup):
        new_gps=[]
        polyline=tup['POLYLINE']
        try:
            new_gps.append([polyline[0][0],polyline[0][1],1])
            for count in range( 0, len(polyline) -1):
                pre=polyline[count]
                nex=polyline[count+1]
                distance= self.haversine(pre[0],pre[1],nex[0],nex[1])
                if distance > 1000:
                    self.out+=1
                    tup['DIRTY']=1
                if distance > 160 :
                    k= ceil(distance/160) - 1
                    for x in range(1,int(k)+1):
                        x=x+0.0
                        new_gps.append([pre[0]-(pre[0]-nex[0])*x/(k+1),pre[1]-(pre[1]-nex[1])*x/(k+1),0]) #lat ,long, added
                        #print (pre[0]-nex[0])*x/(k+1),pre[0],nex[0],x,k
                new_gps.append([nex[0],nex[1],1]) #lat,long,original
            gps=[]
            gps.append(new_gps[0])
            i=0
            while i < len(new_gps)-1 :
                distance = self.haversine(new_gps[i][0],new_gps[i][1],new_gps[i+1][0],new_gps[i+1][1])
                #print distance,"0",i
                j=1
                while distance <100 and i+j+1 < len(new_gps):
                    j+=1
                    
                    distance = self.haversine(new_gps[i][0],new_gps[i][1],new_gps[i+j][0],new_gps[i+j][1])
                    #print distance,"1",i,j
                    if distance>160:
                        j-=1
                
                if i+j >=len(new_gps):
                    gps.append(new_gps[-1])
                else :
                    gps.append(new_gps[i+j])
                i+=j
            #if len(gps)!=len(new_gps):
            #    print len(gps),len(new_gps)
            #print gps
            #print polyline
            tup['POLYLINE']=gps
            return tup
            
        except:
            #print "Len",len(polyline)
            return tup
    def segg(self,tup):
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
