The taxi industry uses electronic dispatch systems to direct taxis from the taxi stands to
the customers. Electronic dispatch systems make it easy to see where a taxi has been, but
not necessarily where it is going. In most cases, taxi drivers operating with an electronic
dispatch system do not indicate the final destination of their current ride or there could
be loss of GPS signal in transit. The presence of information about the final destination
of the trip along with the trip time not only improves the service to the customer but
also is economical for the taxi service. It can also reduce the idle time of taxi drivers
between trips. If a dispatcher knew approximately where their taxi drivers would be
ending their trips, they would be able to identify which taxi to assign to each customer
request and hence could save both time and money by not sending a taxi all the way
from a taxi stand. This project tries to focus only on predicting the final destination of
the taxi rides, given their initial partial trajectories and we leave the trip time prediction
as a task that could be carried out in future to improve the electronic dispatch systems
further. The design and implementation of the various models are discussed along with
their results. A comparison is made between the models and further improvements were
carried out on the most effective model. Further the tasks that could be done in future
are discussed.

Data Set: https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i/data
Data Cleaning: All the steps of data cleaning are carried out by Data Preprocessing/Final_cleaning.py
Data Reduction: Truncation is also carried out in Data Preprocessing/Final_cleaning.py
Support Points: 
k-means clustering is carried out to find support points for start, transition and destination coordinates in Project/Kmeans/Kmeans_n_transition.py
DBSCAN clustering is carried out to find support points for start and destination coordinates in Project/DBSCAN/start_end.py

Seggragate:
Data was seggregated into call type and day types(Project/Seggrate/).
Model:

Training and testing files was created by Project/Model/CreatingTrain_test.py

Matrix:
Testing for both most probable and mean distance is done by Project/Model/Matrix.py

Forest: 
Here Training and Testing, and mean distance is done by Project/Model/Forest.py

Time:
Data is divided into 4 time ranges and start points are plotted(Project/Time/). It was also tested in each time range.
Taxi Groupoing:
Taxi were divided into groups depending upon similarity between them(Project/Taxi_grouping/).
   
Results: 

The result obtained by testing
the model on a month of data which was not used for training gave a result of 2.26 kms.
Also, the result obtained on submitting the model on kaggle was 2.75 kms. The best
score on kaggle was 2.14 kms.
