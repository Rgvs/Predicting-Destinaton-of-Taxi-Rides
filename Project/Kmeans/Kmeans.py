'''
Created at Feb 15th

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
        self.mongo_train = self.mongo_db['cthrvt_160_1min']
        
    def kmeans(self):
        number=0
        X=[]
        Y=[]
        Z=[]
        random_state = 170
        for tup in self.mongo_train.find({"$or":[{'Time.month':9},{'Time.month':10}]}):
            
            number=number+1
            if number%1000==0:
                print (number)
                #if number == 5000:
                    #break
            #for count in range(0,len(tup["POLY"])-1):
            try:            
                if len(tup['POLY'])<30:
                    continue
                #for coordinates in tup["POLY"]:
                #    X.append([float(coordinates[0]),float(coordinates[1]) ])
                X.append([ tup['POLY'][0][0],tup['POLY'][0][1] ])
                Y.append([ tup['POLY'][-1][0],tup['POLY'][-1][1] ])
                Z.append([ tup['POLY'][5][0],tup['POLY'][5][1] ])
            except:
                print (len(tup["POLY"]))
                #time.sleep(2)

        #print X
        print (type(X))
        #X = StandardScaler().fit_transform(X)
        X=np.array(X)
        Y=np.array(Y)
        Z=np.array(Z)
        #print X
        #print X[22][0]
        print (len(X))
        ##############################################################################
        # Compute Kmeans
        
        x_pred = KMeans(n_clusters=150, random_state=random_state).fit(X)
        y_pred = KMeans(n_clusters=150, random_state=random_state).fit(Y)
        z_pred = KMeans(n_clusters=200, random_state=random_state).fit(Z)
        print len(y_pred.cluster_centers_)
        print len(X[:,0])
        #f = open('start_transition_end_K.txt','w')
        #for count in range(0,len(X)-1):
        #    f.write(str(x_pred.labels_[count])+'\t'+str(z_pred.labels_[count])+'\t'+str(y_pred.labels_[count])+'\n')
        f1 = open('K_start.txt','w')
        f2 = open('K_end.txt','w')
        f3 = open('K-transition.txt','w')
        print len(x_pred.cluster_centers_)
        for each in range(0,len(x_pred.cluster_centers_)-1):
            f1.write( str(x_pred.cluster_centers_[each]) +'\n')
            f2.write( str(y_pred.cluster_centers_[each]) +'\n')
        for each in range(0,len(z_pred.cluster_centers_)-1):
            f3.write( str(z_pred.cluster_centers_[each]) +'\n')
            #print x_pred.cluster_centers_[each]
        #plt.scatter(X[:, 0], X[:, 1], c=y_pred.labels_)
        #plt.title("Kmeans")
        #plt.show()
        
if __name__ == '__main__':
    cot = Kmeans()
    cot.kmeans()
