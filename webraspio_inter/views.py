from flask import Flask, render_template, request, redirect, jsonify
import RpiGpio
from webraspio import app, webraspio_global
from intervalo import Intervalo
from helpers import retornastatus, read_api
from web_socket import ativaPorTempo, desativaTempo, ativaIntervalo
import requests
import simplejson
import json


RpiGpio.inicia()

@app.route('/', methods=["GET", "POST"])
def index():
    global webraspio_global

    if request.method == "POST":
        if request.form.get('setTemp'):
            webraspio_global['setTemp'] = float(request.form.get('setTemp'))

        webraspio_global['tempEnabled'] = bool(request.form.get('tempE'))

    if webraspio_global['tempEnabled']:
        temp = read_api()

        if temp > webraspio_global['setTemp']:
            # webraspio_global['statusSaida1'] = RpiGpio.ativa()
            return redirect('/saida1/on')
        else:
            # webraspio_global['statusSaida1'] = RpiGpio.desativa()
            return redirect('/saida1/off')
        
    return retornastatus()


@app.route("/saida1/on")
def actionSaida1On():
    global webraspio_global
    webraspio_global['statusSaida1'] = RpiGpio.ativa()

    if webraspio_global['tempEnabled']:
        temp = read_api()

        if temp < webraspio_global['setTemp']:
            webraspio_global['statusSaida1'] = RpiGpio.desativa()
            return redirect('/saida1/off')

    return retornastatus()


@app.route("/saida1/off")
def actionSaida1Off():
    global webraspio_global
    webraspio_global['statusSaida1'] = RpiGpio.desativa()
    webraspio_global['stsTempo'] = 'desativado'
    desativaTempo()
    if webraspio_global['tempEnabled']:
        temp = read_api()

        if temp > webraspio_global['setTemp']:
            webraspio_global['statusSaida1'] = RpiGpio.ativa()
            return redirect('/saida1/on')

    return retornastatus()


@app.route("/saida1/onT", methods=["GET", "POST"])
def actionGetTempo():
    global webraspio_global

    if request.method == "POST":
        req = request.form
        webraspio_global['tempo'] = int(req.get("txt_tempo"))
        if not webraspio_global['tempo']:
            print("Error empty")
        else:
            if webraspio_global['tempo'] > 0:
                webraspio_global['tempo'] = webraspio_global['tempo'] * 60
                ativaPorTempo()  # tempo em minutos

    return render_template('webraspio.html', tempo= (int(webraspio_global['tempo']/60)))


@app.route("/saida1/intervalo", methods=["GET", "POST"])
def actionIntervalo():
    global webraspio_global

    if request.method == "POST":
        req = request.form
        
        t_off = int(req.get("txt_freq_ligar"))
        t_on = int(req.get("txt_tempo_ligado"))
        repetir = int(req.get("txt_repetir"))

        if not t_off or not t_on or not repetir or t_off > 60:
            print("Error Intervalo empty")
        elif t_off > 60:
            print("Error Intervalo - t_off > 60")
        else:
            inter = Intervalo(t_off*60, t_on*60, repetir)

            webraspio_global['inter'] = True
            webraspio_global['objInter'] = inter
            inter.start_intervalo()

    return render_template('webraspio.html', vezes_i= (int(inter.repetir)))
