from flask import Flask, render_template

from webraspio import webraspio_global

import requests
import simplejson
import json

def retornastatus():
    global webraspio_global

    statuspin = {'statusSaida1': webraspio_global['statusSaida1'],
                 'stsTempo': webraspio_global['stsTempo'],
                 'stsIntervalo': webraspio_global['stsIntervalo'],
                 'temp': webraspio_global['temp'],
                 'tempEn': webraspio_global['tempEnabled'],
                 'setT': webraspio_global['setTemp'],
                 }

    return render_template('webraspio.html', **statuspin)

def read_api():

    date = {'temp':None}
    temp = -1.0
    global webraspio_global
    uri = "http://rpi3:8001/api/temp"

    try:
        uResp = requests.get(uri)
        Jresp = uResp.text
        date = json.loads(Jresp)
        temp = float(date['temp'])
        webraspio_global['temp'] = temp
    except:
        temp = -1
        webraspio_global['tempEnabled'] = False
        print('Connection Error')

    return temp
