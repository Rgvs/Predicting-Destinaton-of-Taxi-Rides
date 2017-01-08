'''
Created at Feb 15th

'''
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import pytz
import csv
from pymongo.mongo_client import MongoClient
import time,datetime,pymongo


from math import radians, cos, sin, asin, sqrt, ceil

class Dbscan:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['cthrvt_160_1min']
        
    def db(self):
        number=0
        X=[]
        Y=[]
        Z=[]
        for tup in self.mongo_train.find({"$or":[{'Time.month':9},{'Time.month':10}]}):
            # Generate sample data
            #print "yes"
            number=number+1
            if number%1000==0:
                print (number)
                #if number == 20000:
                #    break
            #for count in range(0,len(tup["POLY"])-1):
            try:            
                if len(tup['POLY'])<30:
                    continue
                X.append([tup["POLY"][0][0],tup["POLY"][0][1]])
                Y.append([tup["POLY"][-1][0],tup["POLY"][-1][1]])
                Z.append([tup["POLY"][5][0],tup["POLY"][5][1]])
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
        # Compute DBSCAN_X
        db = DBSCAN(eps=0.0003, min_samples=10).fit(X)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        labelsx = labels 
        length=db.core_sample_indices_
        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        print (len(db.core_sample_indices_))
        print (len(db.labels_))
        p=[]
        for a in range(0,n_clusters_):
            p.append(0)
        for a in range(0,n_clusters_):
            p[a]=[]
        #print p
        for i in range(0,len(labels) - 1) :
            if(labels[i] != -1) :
                p[labels[i]].append(X[i])
        meanx = []
        m1x=[]
        m2x=[]
        for i in range(0,n_clusters_):
            m=0.0
            n =0.0
            for k in p[i]:
                m = m + float(k[0])
                n = n+ float(k[1])
            m=m/len(p[i])
            n = n/len(p[i])
            meanx.append([m,n])
            m1x.append(m)
            m2x.append(n)
        meanx.append([0,0])
        #f = open('Start','w')
        #for a in meanx:
        #    a=str(a)+'\n'
        #    f.write(a) # python will convert \n to os.linesep
        #f.close()
        ####################################################################
        
        db = DBSCAN(eps=0.0003, min_samples=10).fit(Y)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labelsy = db.labels_
        
        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labelsy)) - (1 if -1 in labels else 0)
        print len(db.core_sample_indices_)
        print len(db.labels_)
        p=[]
        for a in range(0,n_clusters_):
            p.append(0)
        for a in range(0,n_clusters_):
            p[a]=[]
        #print p
        for i in range(0,len(labelsy) - 1) :
            if(labelsy[i] != -1) :
                p[labelsy[i]].append(X[i])
        meany = []
        m1y=[]
        m2y=[]
        for i in range(0,n_clusters_):
            m=0.0
            n =0.0
            for k in p[i]:
                m = m + float(k[0])
                n = n+ float(k[1])
            m=m/len(p[i])
            n = n/len(p[i])
            meany.append([m,n])
            m1y.append(m)
            m2y.append(n)
        meany.append([0,0])
    
            
        db = DBSCAN(eps=0.0004, min_samples=10).fit(Z)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labelsz = db.labels_
        length=db.core_sample_indices_
        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labelsz)) - (1 if -1 in labels else 0)
        print (len(db.core_sample_indices_))
        print (len(db.labels_))
        p=[]
        for a in range(0,n_clusters_):
            p.append(0)
        for a in range(0,n_clusters_):
            p[a]=[]
        #print p
        for i in range(0,len(labelsz) - 1) :
            if(labelsz[i] != -1) :
                p[labelsz[i]].append(X[i])
        meanz = []
        m1z=[]
        m2z=[]
        for i in range(0,n_clusters_):
            m=0.0
            n =0.0
            for k in p[i]:
                m = m + float(k[0])
                n = n+ float(k[1])
            m=m/len(p[i])
            n = n/len(p[i])
            meanz.append([m,n])
            m1z.append(m)
            m2z.append(n)
        meanz.append([0,0])
            
        f = open('matching_start_transition_end_model.txt','w')
        f1 = open('start_model.txt','w')
        f2 = open('transition_model.txt','w')
        f3 = open('end_model.txt','w')
        #print len(labelsz)
        #print len(labelsy)
        #print len(labelsx)
        for each in range(0,len(labelsx)):
            a=str(X[each])+'\t'
            a=a+str(labelsx[each])+'\t'
            a=a+str(meanx[labelsx[each]])+'\t'
            a=a+str(Z[each])+'\t'
            a=a+str(labelsz[each])+'\t'
            a=a+str(meanz[labelsz[each]])+'\t'
            a=a+str(Y[each])+'\t'
            a=a+str(labelsy[each])+'\t'
            a=a+str(meany[labelsy[each]])+'\n'
            f.write(a) # python will convert \n to os.linesep
        f.close()
        for each in meanx:
            f1.write(str(each)+'\n')
        for each in meany:
            f2.write(str(each)+'\n')
        for each in meanz:
            f3.write(str(each)+'\n')

        f1.close()
        f2.close()
        f3.close()
        print('Estimated number of clusters: %d' % n_clusters_)
        ##############################################################################


if __name__ == '__main__':
    cot = Dbscan()
    cot.db()
