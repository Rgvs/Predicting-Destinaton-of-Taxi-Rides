from math import radians, cos, sin, asin, sqrt, ceil
f=open("K_n_transition_K_DA_CA.txt","r")
k=[]
for line in f:
    line=line.split()
    k.append([float(line[0]),float(line[1])])
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

smallest=10000000
    
for i in k:
    smallest=10000000
    for j in k:
        dist=haversine(i[0],i[1],j[0],j[1])
        if(dist<smallest and dist!=0):
            smallest=dist
            if(dist>10000):
                print i,j   
    if smallest<150:
        print smallest
