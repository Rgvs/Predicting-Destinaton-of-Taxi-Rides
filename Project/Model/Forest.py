from math import radians, cos, sin, asin, sqrt, ceil
class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.weight=1

    def add_child(self, obj):
        flag=0
        #print obj.data
        for i in range(0,len(self.children)):
            if self.children[i].data == obj.data:
                self.children[i].weight+=1
                #print i
                flag=1
                break
        if flag==0:
            self.children.append(obj)
    def get_leaf(self):
        q=[]
        for a in self.children:
            q.append(a)
        leaf=[]
        i=0
        if len(q)==0:
            print "ZERO"
        while i<len(q):
            a=q[i]
            if len(a.children) ==0:
                leaf.append(a)
                i+=1
                continue
            for child in a.children:
                q.append(child)
            #print len(self.children)
            i+=1
        return leaf
start=[]
for i in range(0,250):
    start.append(Node(i))
    
def haversine(lon1, lat1, lon2, lat2):
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
       
f = open("trainB1.txt","r")

for line in f:
    line=line.split()
    x=start[int(line[0])]
    for i in range(1,len(line)):
        if i+2<len(line) and line[i]==line[i+1]:
            continue
        x.add_child(Node(int(line[i])))
        #print line[i]
        for j in range(0,len(x.children)):
            if x.children[j].data == int(line[i]):
                x=x.children[j]
                break
f = open("Actual_endB2.txt","r")
end=[]
for line in f:
    line=line.split()
    end.append( [ float(line[0]) ,float(line[1]) ] )
f = open("testB2.txt","r")
number=-1
inside=0
total_dist=0.0
count_good=count_avg=count_bad=0
for line in f:
    
    line=line.split()
    x=start[int(line[0])]
    #print x.data
    for i in range(1,len(line)):
        flag=0
        for j in range(0,len(x.children)):
            if x.children[j].data == int(line[i]):
                x=x.children[j]
                flag=1
                #print x.data,start[int(line[0])].data
                break
        if flag==0:
            break
    a=x.get_leaf()
    number+=1
    if len(a) ==0 :
        print x.data,line
        #print line
        continue
    inside+=1
    total_weight=0.0
    x=0.0
    y=0.0
    
    for leaf in a:
        x += end[leaf.data][0] * leaf.weight
        y += end[leaf.data][1] * leaf.weight
        total_weight+=leaf.weight
    dist=haversine(x/total_weight,y/total_weight,end[number][0],end[number][1])
    if dist <2000:
        count_good+=1
    elif dist <5000:
        count_avg+=1
    else:
        count_bad+=1 
    total_dist+=dist
    #print dist,number
    #if dist >10000:
        #print line,end[number],len(a)
    #break
print total_dist/(inside),inside,number,count_good,count_avg,count_bad

