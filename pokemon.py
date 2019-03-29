from flask import Flask, request
from cassandra.cluster import Cluster
import requests
import json
cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)
#show the hello word
@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))
#get the data from API and store in cassandra
@app.route('/airqualitychart', methods=['GET'])
def profile():
    #This is the API of air quality forecast
    Air_url_template = 'https://api.breezometer.com/air-quality/v2/forecast/hourly?lat={lat}&lon={lon}&key={API_KEY}&hours={number_of_forecast_hours}'
    #set the location
    my_latitude = request.args.get('lat','48.857456')
    my_longitude = request.args.get('lon','2.354611')
    num = request.args.get('hours','24')
    #The key of API
    MY_API_KEY = '9d6642727af946669166f5af6fcd2302'
    #get the data from API
    air_url = Air_url_template.format(lat=my_latitude, lon=my_longitude,API_KEY=MY_API_KEY,number_of_forecast_hours=num)
    resp = requests.get(air_url)
    #The data is stored as a json file
    if resp.ok:
        air_json=resp.json()
    else:
        print(resp.reason)
    #select the data and store as a dictionary{datetime:aqi}
    categories = {categ["datetime"]:categ["indexes"]["baqi"]["aqi"] for categ in air_json["data"]}
    #put data into the cassandra database
    for i in categories:
        rows = session.execute( """INSERT INTO pokemon.stats(datetime,aqi) values('{}',{})""".format(i,categories[i]))
    return('<h1>{}</h1>'.format(air_json))
#select from the database,find the best air quality in the future 24 hours
@app.route('/airqualitychart/best')
def airq():
    #select the data which has the largest aqi
    air=session.execute("""Select datetime,max(aqi) from pokemon.stats""")
    for qu in air:
        return('<h1>The best air quality in the next 24 hours is on {}.</h1>'.format(qu.datetime))
    #return('<h1>{}</h1>'.format(categories))
#Get the air quality of the time
@app.route('/airqualitychart/best/<time>')
def airtime(time):
    #select the air quality due to the time
    ta = session.execute( """Select * From pokemon.stats where datetime = '{}'""".format(time))
    for p in ta:
        return('<h1>{} has the air quality of {}.</h1>'.format(time,p.aqi))
    return('<h1>That time does not exist!</h1>')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
