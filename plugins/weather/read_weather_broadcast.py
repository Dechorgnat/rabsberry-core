#!/usr/bin/python
# -*- coding: utf-8 -*-

# Nous commencons par inclure les librairies que nous avons installées.
import urllib
import requests
from core.functions.play_tts import play_tts
from core.functions.play_audio import play_audio_files
from core.tools.config import getConfig

conf = getConfig()

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

# Nous construisons le texte à réciter.
text = u"Bulletin météo : " + resp['weather'][0]['description']

# Ensuite, nous ajoutons la température pour conclure la phrase. Notez, que nous l'arrondissons.
text = text + u". A Rennes, il fait actuellement "+ str(resp['main']['temp']).replace('.',',') +u" degrés."

#print text

play_audio_files([ conf['CORE_ROOT'] + "/resources/mp3/weather/fr/signature.mp3"])
play_tts(text.encode('utf8'), 'fr')
play_audio_files([ conf['CORE_ROOT'] + "/resources/mp3/weather/fr/signature.mp3"])
