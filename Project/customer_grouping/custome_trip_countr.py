from pymongo.mongo_client import MongoClient
import time,datetime,pymongo
class Customer:
    
    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017)
        self.mongo_db = self.mongo_client['taxi']
        self.mongo_test = self.mongo_db['test']
        self.mongo_train = self.mongo_db['160_calltype_A']
    def customer(self):
        customer_id= []
        for tup in self.mongo_train.find():
            try:
                customer_id.append(tup["ORIGIN_CALL"])
            except:
                pass
        customerfreq = []
        for w in customer_id:
            customerfreq.append(customer_id.count(w))
        ls=list(set(zip(customer_id, customerfreq)))
        count =0
        for a, b in ls:
            if(b<5):
                count+=1
            print (str(a) +"\t" + str(b))
            
        print count , len(ls)
if __name__ == '__main__':
    cot = Customer()
    cot.customer()
        
