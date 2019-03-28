from flask import Flask, request
from cassandra.cluster import Cluster
import requests
import json
cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)
@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))

@app.route('/airqualitychart', methods=['GET'])
def profile():
    Air_url_template = 'https://api.breezometer.com/air-quality/v2/forecast/hourly?lat={lat}&lon={lon}&key={API_KEY}&hours={number_of_forecast_hours}'
    my_latitude = request.args.get('lat','48.857456')
    my_longitude = request.args.get('lon','2.354611')
    num = request.args.get('hours','24')
    MY_API_KEY = '9d6642727af946669166f5af6fcd2302'
    #air_url = Air_url_template.format(lat=my_latitude, lon=my_longitude,API_KEY=app.config['MY_API_KEY'],number_of_forecast_hours=num)
    air_url = Air_url_template.format(lat=my_latitude, lon=my_longitude,API_KEY=MY_API_KEY,number_of_forecast_hours=num)
    resp = requests.get(air_url)

    if resp.ok:
        air_json=resp.json()
    else:
        print(resp.reason)

    categories = {categ["datetime"]:categ["indexes"]["baqi"]["aqi"] for categ in air_json["data"]}
    for i in categories:
        rows = session.execute( """INSERT INTO pokemon.stats(datetime,aqi) values('{}',{})""".format(i,categories[i]))
    return('<h1>Data has been load.</h1>')

@app.route('/airqualitychart/best')
def airq():
    air=session.execute("""Select datetime,max(aqi) from pokemon.stats""")
    for qu in air:
        return('<h1>The best air quality in the next 24 hours is on {}.</h1>'.format(qu.datetime))
    #return('<h1>{}</h1>'.format(categories))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
