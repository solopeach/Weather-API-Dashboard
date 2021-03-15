import requests
import configparser
from flask import request
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def weather_dashboard():
    return render_template('home.html')   

@app.route('/results', methods = ['POST'])
def render_results():
    zip_code = request.form['zipCode']

    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"]) 
    #float with 2 decimal places, string
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    #essentially parsing json data
    weather = data["weather"][0]["main"]
    location = data["name"]
    icon = data["weather"][0]["icon"]

    return render_template('results.html', location=location, temp=temp, feels_like=feels_like, weather=weather, icon=icon)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_results(zip_code, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

if __name__ == '__main__':
    app.run()


    
