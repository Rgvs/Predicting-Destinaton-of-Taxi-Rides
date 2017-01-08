'''
Created at Feb 15th
Modified on Feb 22nd
'''
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo


from math import radians, cos, sin, asin, sqrt, ceil

class Kmeans:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['160_daytype_A_calltype_A']
        
    def kmeans(self):
        number=0
        X=[]
        Y=[]
        Z=[]
        sZ=[0]
        random_state = 170
        #for tup in self.mongo_train.find( {"$and" : [ 
        #                                    { "$or": [ 
        #                                        {'Time.month':9}, 
        #                                        {'Time.month':10} 
        #                                        ] } , 
        #                                    {'CALL_TYPE': 'C'}
        #                                    ]}):
        for tup in self.mongo_train.find({"$and":[ {"$or":[{'TIME.month':11},{'TIME.month':12}]} , {'TIME.hour':{"$lt":12} } ] }):    
            number=number+1
            if number%1000==0:
                print (number)
                if number == 90000:
                    print tup['TIME']
                    #break
            #for count in range(0,len(tup["POLY"])-1):
            try:
                if len(tup['POLYLINE'])/4 < 8:
                    continue
                #for coordinates in tup["POLY"]:
                #    X.append([float(coordinates[0]),float(coordinates[1]) ])
                X.append([ tup['POLYLINE'][0][0],tup['POLYLINE'][0][1] ])
                Y.append([ tup['POLYLINE'][-1][0],tup['POLYLINE'][-1][1] ])
                count=0
                for coordinates in tup['POLYLINE'][1:-1]:
                    count+=1
                    if count%4==0:
                        Z.append([ coordinates[0],coordinates[1] ])
                    
                sZ.append(len(Z)-sum(sZ))
            except:
                print (len(tup["POLYLINE"]))
                #time.sleep(2)
        #print X
        print (type(X))
        #X = StandardScaler().fit_transform(X)
        X=np.array(X)
        Y=np.array(Y)
        Z=np.array(Z)
        #print X
        print len(Z)
        print (len(X))
        ##############################################################################
        # Compute Kmeans
        
        x_pred = KMeans(n_clusters=250, random_state=random_state).fit(X)
        y_pred = KMeans(n_clusters=250, random_state=random_state).fit(Y)
        
        z_pred = KMeans(n_clusters=400, random_state=random_state).fit(Z)
        #plt.scatter(Z[:, 0], Z[:, 1], c=z_pred.labels_)
        #plt.title("K-means clustering of transition points for Sept & Oct")
        #plt.savefig("Sept_oct_kmeans_trans.png")
        
        #print len(y_pred.cluster_centers_)
        #print len(X[:,0])
        
        
        f = open('start_n_transition_end1.txt','w')
        for count in range(0,len(X)):
            f.write(str(x_pred.labels_[count])+'\t')
            sum_sZ=sum(sZ[0:count])
            for each in range(0,sZ[count+1]):
                f.write( str(z_pred.labels_[sum_sZ+each]) +'\t')
            f.write( str(y_pred.labels_[count])+'\n')
        f1 = open('K_start1.txt','w')
        f2 = open('K_end1.txt','w')
        f3 = open('K_n_transition1.txt','w')
        #print len(x_pred.cluster_centers_)
        for each in range(0,len(x_pred.cluster_centers_)):
            f1.write( str(x_pred.cluster_centers_[each][0])+"\t"+str(x_pred.cluster_centers_[each][1]) +'\n')
            f2.write( str(y_pred.cluster_centers_[each][0])+"\t"+str(y_pred.cluster_centers_[each][1]) +'\n')
        for each in range(0,len(z_pred.cluster_centers_)):
            f3.write( str(z_pred.cluster_centers_[each][0])+"\t"+str(z_pred.cluster_centers_[each][1]) +'\n')
            #print x_pred.cluster_centers_[each]
        
        
if __name__ == '__main__':
    cot = Kmeans()
    cot.kmeans()
