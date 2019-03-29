A Flask app using air quality API that needs authentication!

The app is written in the pokemon.app.

First I get the data from the API.

The API is in the form of  'https://api.breezometer.com/air-quality/v2/forecast/hourly?lat={lat}&lon={lon}&key={API_KEY}&hours={number_of_forecast_hours}'. 

Lat and lon is the location, hours is the hour you want to predict.

Make sure you have the key from the web API.

The data from the API is stored as a json file.

Then the data I want to use is put into a dictionary. {datetime,aqi}

Use the URL:http://external IP/airqualitychart, you can see the json file. 

Then I insert into cassandra database.(need to create a table on cloud to store data)
the terminal instruction is: 

    ```CREATE KEYSPACE pokemon WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 2};```
    
    ```CREATE TABLE pokemon.stats (datetime text PRIMARY KEY, aqi int);```

The instruction is under cqlsh inside the container(names may be different from the example): 

    ```kubectl exec -it cassandra-bk794 cqlsh'''
    

The database has two columes(datetime,aqi).

I select the max aqi which means the best air quality.

I show the time in the next 24 hours which has the best air quality.

Use the URL:http://external IP/airqualitychart/best you can see the best time.

If you want to see the air quality of any time, you can go to http://external IP/airqualitychart/best/<time>, where the 'time' in the URL is the time you want.

Here is the detail process:

1.Create a subdirectory on your Google shell computer, e.g.: mkdir mini_project && mini_project 

2.Set the region and zone for our new cluster && export the project name as an environment variable for later ease of access

    ```gcloud config set compute/zone europe-west2-b```

    ```export PROJECT_ID="$(gcloud config get-value project -q)"```
    
3. Creates a 3 node cluster named cassandra: 
    
    ```gcloud container clusters create cassandra --num-nodes=3 --machine-type "n1-standard-2"```
    
4. Download Kubernetes service:
    
    ```wget -O cassandra-peer-service.yml http://tinyurl.com/yyxnephy```
    
    ```wget -O cassandra-service.yml http://tinyurl.com/y65czz8e```
    
    ```wget -O cassandra-replication-controller.yml http://tinyurl.com/y2crfsl8```
    
5.Run the three components:
    
    ```kubectl create -f cassandra-peer-service.yml```
    
    ```kubectl create -f cassandra-service.yml```
    
    ```kubectl create -f cassandra-replication-controller.yml```
    
6. Scale up our number of nodes via our replication-controller:
    
    ```kubectl scale rc cassandra --replicas=3```
  
7.Check that the three containers are running correctly and get their names:

    ```kubectl get pods -l name=cassandra```
    
8.Run cqlsh inside the container(name may be different from the example):

    ```kubectl exec -it cassandra-bk794 cqlsh```
 
9.Build our keyspace:
    
    ```CREATE KEYSPACE pokemon WITH REPLICATION ={'class' : 'SimpleStrategy', 'replication_factor' : 2};```
    
10.Create the table for our stats:

    ```CREATE TABLE pokemon.stats (datetime text PRIMARY KEY, aqi int);```
    
11.Build image:

    ```docker build -t gcr.io/${PROJECT_ID}/pokemon-app:v1 .```
    
12.Push it to the Google Repository:

    ```docker push gcr.io/${PROJECT_ID}/pokemon-app:v1```
    
13.Run it as a service:

    ```kubectl run pokemon-app --image=gcr.io/${PROJECT_ID}/pokemon-app:v1 --port 8080```
    
14.Expose the deploment to get an external IP:

    ```kubectl expose deployment pokemon-app --type=LoadBalancer --port 80 --target-port 8080```

    
