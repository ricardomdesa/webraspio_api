from flask_socketio import SocketIO, emit

from flask import Flask, render_template, request

from threading import Thread, Event

import RpiGpio

app = Flask(__name__)

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#time Thread
thread = Thread()
thread_stop_event = Event()

statuspin = {'statusSaida1': False,
             'stsTempo': False
             }

RpiGpio.inicia()

tempo = 0
stsTempo = "desativado"
statusSaida1 = 'off'
horaInicio = 0
cont = 0

def timeRele():
    global tempo
    global cont
    global statusSaida1
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():

        if tempo is not 0:
            socketio.sleep(1)
            cont = cont + 1
            socketio.emit('newnumber', {'cont': cont, 'tempo': tempo}, namespace='/test')
            if cont == tempo:
                tempo = 0
                cont = 0
                statusSaida1 = RpiGpio.desativa()
                socketio.emit('newnumber', {'cont': cont, 'tempo': tempo}, namespace='/test')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')
    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(timeRele)



@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


@app.route('/')
def index():
    tempdata = {
        'title': 'RPi GPIO Control'
    }
    return retornastatus()


@app.route("/saida1/on")
def actionSaida1On():
    global statusSaida1
    statusSaida1 = RpiGpio.ativa()
    return retornastatus()


@app.route("/saida1/off")
def actionSaida1Off():
    global statusSaida1
    statusSaida1 = RpiGpio.desativa()
    return retornastatus()


@app.route("/saida1/onT", methods=["GET", "POST"])
def actionGetTempo():
    global tempo
    global horaInicio
    if request.method == "POST":
        req = request.form
        tempo = int(req.get("txt_tempo"))
        if not tempo:
            print("Error empty")
        else:
            if tempo > 0:
                tempo = tempo * 60
                ativaPorTempo()  # tempo em minutos

    return render_template('webraspio.html', tempo= (tempo/60))

def ativaPorTempo():
    global stsTempo
    global thread
    global statusSaida1

    statusSaida1 = RpiGpio.ativa()
    stsTempo = "ativado"

    def fnc1():
        global statusSaida1
        statusSaida1 = RpiGpio.desativa()

    stsTempo = "desativado"

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(timeRele)


def retornastatus():
    global stsTempo
    global tempo
    global statusSaida1

    statuspin = {'statusSaida1': statusSaida1,
                 'stsTempo': stsTempo
                 }

    return render_template('webraspio.html', **statuspin)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
