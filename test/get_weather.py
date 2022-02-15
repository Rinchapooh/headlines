import json
import urllib.request
from pprint import pprint

import requests


def ger_weather(city):
    api_url = "https://openexchangerates.org//api/latest.json?app_id=70e97f32457f47d9b348254bc5da3978"
    # api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=8a691ca8687d5da894a462b99705f045"
    resp = requests.get(api_url)
    data = resp.json()
    '''weather = {'description': data["weather"][0]["description"],
               'temperature': data["main"]["temp"],
               'city': data["name"],
               'country': data['sys']['country'],
               'wind': data['wind']['speed']
               }'''
    # res = json.loads(data)

    parsed = json.loads(data).get('rates')
    pprint(parsed)
    # print(json.dump(res, indent=4, sort_keys=True))


def get_rate(frm, to):
    api_url = "https://openexchangerates.org/api/latest.json?app_id=70e97f32457f47d9b348254bc5da3978"
    resp = requests.get(api_url)
    data = resp.json()
    all_currency = (data['rates'])
    frm_rate = all_currency.get(frm.upper())
    to_rate = all_currency.get(to.upper())
    keys_rate = all_currency.keys()
    x = frm_rate/to_rate
    #print(round(x, 2))
    pprint(keys_rate)
    return frm_rate / to_rate


get_rate('KZT', 'USD')
