A Flask app using air quality API that needs authentication!
The app is written in the pokemon.app.
First I get the data from the API.
Then I insert into cassandra database.
The database has two columes(datetime,aqi).
I select the max aqi which means the best air quality.
Finally I show the time in the next 24 hours which has the best air quality.
