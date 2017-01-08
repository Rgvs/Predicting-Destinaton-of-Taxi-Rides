'''
Created at Feb 16th
Modified on Feb 23rd
'''
from math import radians, cos, sin, asin, sqrt, ceil

class Fixing:
    
    '''
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['cthrvt_160_1min']
        
    '''
    
    def fix(self):
        number=0
        self.s_coordinates=[]
        self.e_coordinates=[]
        self.s_labels=[]
        self.e_labels=[]
        self.start_coordinates=[]
        self.end_coordinates=[]
        self.read_end()
        self.read_start()
        self.read_coordinates()
        self.fix_start()
        self.fix_end()
        
        
    def fix_start(self):
        
        for i in range(0,len(self.s_labels)):
            
            if (self.s_labels[i] == -1):
                min_dist=50000
                j=0
                #print i
                for support in self.start_coordinates:
                    #print support
                    distance=self.haversine ( support[0], support[1], self.s_coordinates[i][0], self.s_coordinates[i][1] )
                    #print distance
                    if( distance < min_dist):
                        min_dist=distance
                        self.s_labels[i]=j
                    j=j+1
                #if (j != 0):
                #    print self.s_labels[i]
            if (i%1000==0):
                print i
        f = open('start_fixed.txt', 'w')
        for i in self.s_labels:
            f.write(str(i)+'\n')
        f.close()

    def fix_end(self):
        for i in range(0,len(self.e_labels)):
            if (self.e_labels[i] == -1):
                min_dist=50000
                j=0
                #print i
                for support in self.end_coordinates:
                    #print support
                    distance=self.haversine ( support[0], support[1], self.e_coordinates[i][0], self.e_coordinates[i][1] )
                    #print distance
                    if( distance < min_dist):
                        min_dist=distance
                        self.e_labels[i]=j
                    j=j+1
                #if (j != 0):
                #    print self.e_labels[i]
            if (i%1000==0):
                print i
        f = open('end_fixed.txt', 'w')
        for i in self.e_labels:
            f.write(str(i)+'\n')
        f.close()

    def haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km*1000
        """
        distance = sqrt((lon1-lon2)*(lon1-lon2) + (lat1-lat2)*(lat1-lat2))
        return distance
    def read_coordinates(self):
        f = open('db_matching_start_end.txt', 'r')
        for line in f:
            line=line.split()
            #print line
            
            self.s_coordinates.append([ line[0], line[1] ])
            self.e_coordinates.append([ line[3], line[4] ])
            self.s_labels.append(line[2])
            self.e_labels.append(line[5])
        f.close()
    
    def read_start(self):
        f = open('db_start.txt', 'r')
        for line in f:
            line=line.split()
            self.start_coordinates.append( [ line[0], line[1] ] )
        f.close()
        
    def read_end(self):
        f = open('db_end.txt', 'r')
        for line in f:
            line=line.split()
            self.end_coordinates.append( [ line[0], line[1] ] )
        f.close()
        
if __name__ == '__main__':
    cot = Fixing()
    cot.fix()
