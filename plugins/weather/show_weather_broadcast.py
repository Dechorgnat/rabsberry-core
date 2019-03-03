#!/usr/bin/python
# -*- coding: utf-8 -*-

# Nous commencons par inclure les librairies que nous avons installées.
import urllib
import requests
import json;
from Rabsberry.core.tools.config import getConfig
import paho.mqtt.client as paho

#conf = getConfig()

# Nous construisons ensuite la requête pour obtenir le temps actuel.
openWeatherMapQuery = {
    'q': 'Rennes, France',
    'lang': 'fr',
    'units': 'metric',
    'appid': '0885ba357698e289ada592480c0cb75e'
}
openWeatherMapURL = "http://api.openweathermap.org/data/2.5/weather?"+ urllib.urlencode(openWeatherMapQuery)

# Nous procédons ensuite à la requête de l'API.
r = requests.get(openWeatherMapURL)
if r.status_code >= 400 :
    print "Failed to call openWeatherMapURL on ",openWeatherMapURL
    exit(1)

resp=r.json()
print resp

condition = resp['weather'][0]['main']
if condition == 'Rain':
    condition = 'pluie'
elif condition == 'Clear':
    condition = 'soleil'
elif condition == 'Clouds':
    condition = 'nuage'
elif condition == 'Snow':
    condition = 'neige'
elif condition == 'Mist' or condition == 'Fog':
    condition = 'brouillard'
elif condition == 'Thunderstorm':
    condition = 'orage'

# init mqtt connection and subscribe
broker="127.0.0.1"
client = paho.Client("show_weather")  # create client
client.connect(broker)  # connect
message = {"command": "pattern", "pattern": condition}
client.publish("leds",json.dumps(message))
print json.dumps(message)
