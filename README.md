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
    [the terminal instruction is: CREATE KEYSPACE pokemon WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 2};
                                  CREATE TABLE pokemon.stats (datetime text PRIMARY KEY, aqi int); ]
The instruction is under cqlsh inside the container: kubectl exec -it cassandra-bk794 cqlsh(names may be different from the example).
The database has two columes(datetime,aqi).
I select the max aqi which means the best air quality.
I show the time in the next 24 hours which has the best air quality.
Use the URL:http://external IP/airqualitychart/best you can see the best time.
If you want to see the air quality of any time, you can go to http://external IP/airqualitychart/best/<time>, where the 'time' in the URL is the time you want.
