from flask import Flask, request

# import json
# import requests

from cassandra.cluster import Cluster

cluster = Cluster(['cassandra'])
session = cluster.connect()


app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))



@app.route('/airqualitychart', methods=['GET'])
def airchart():
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
       rows = session.execute( """INSERT INTO pokemon.stats(datetime,aqi) value('{}',{})""".format(i,categories[i]))
    cha= session.execute("""Select * From pokemon.stats""")
    Max = session.execute("""Select * From pokemon.stats where aqi=max(aqi)""")
    for j in Max:
       return('<h1>Here is the best air quality {} in the next 24 hours{}.</h1>'.format(j.aqi,j.datetime))
    return('<h1>{}</h1>'.format(air_json))
    return jsonify(air_json)
    return('done')
    return('<h1>{} has the best airquality{}!</h1>'.format(date,z))
    return('<h1>Here is the best air quality in the next 24 hours.{}</h1>'.format(sorted_cate[0]))
if __name__=="__main__":
    app.run(port=8080, debug=True)