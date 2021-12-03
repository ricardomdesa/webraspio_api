from flask_socketio import SocketIO, emit
from threading import Thread, Event
from webraspio import webraspio_global, app
import RpiGpio
from helpers import retornastatus

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#time Thread
thread = Thread()
thread_stop_event = Event()

def timeRele():
    global webraspio_global
    cont = 0
    restante_s = 0
    restante_m = 0

    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop
    print('=============='+"Making random numbers")
    while not thread_stop_event.isSet():

        if webraspio_global['tempo'] is not 0 and webraspio_global['stsTempo'] != 'desativado':
            socketio.sleep(1)
            cont = cont + 1
            restante_s = webraspio_global['tempo'] - cont
            restante_m = int(restante_s/60)
            socketio.emit('newnumber', {'cont': restante_s, 'tempo': restante_m}, namespace='/test')

            # se o tempo acabar:
            if cont == webraspio_global['tempo']:
                webraspio_global['tempo'] = 0
                cont = 0
                webraspio_global['statusSaida1'] = RpiGpio.desativa()
                webraspio_global['stsTempo'] = 'desativado'
                socketio.emit('newnumber', {'cont': 0, 'tempo': 0}, namespace='/test')
        else:
            cont = 0


def timeReleInter(inter):
    global webraspio_global

    inter = webraspio_global['objInter']
    if not inter:
        print('Fail inter')
    else:
        print('\n ========== Intervalo time =====\n')

        t_total = inter.t_on + inter.t_off
        stsInter = True

        while not thread_stop_event.isSet():
            if webraspio_global['inter']:
                for i in range(0, inter.repetir):
                    for j in range(0, t_total):
                        if j < inter.t_on:
                            socketio.sleep(1)
                            webraspio_global['statusSaida1'] = RpiGpio.ativa()
                            webraspio_global['stsTempo'] = 'ativado'
                            stsInter = True
                            print('Inter on')
                            # inter.ligado()
                        if j >= inter.t_on and j < inter.t_off:
                            socketio.sleep(1)
                            webraspio_global['statusSaida1'] = RpiGpio.desativa()
                            webraspio_global['stsTempo'] = 'desativado'
                            print('Inter off')
                            # inter.desligado()
                        socketio.emit('intervalo', {'t_on': inter.t_on, 't_off':inter.t_off, 'repetir': inter.repetir, 'stsInter': stsInter}, namespace='/test')
                    
                    #termina o intervalo
                    if i == inter.repetir - 1:
                        webraspio_global['stsIntervalo'] = "desativado"
                        stsInter = False
                        webraspio_global['objInter'] = None
                        webraspio_global['inter'] = False
                        print('Finishing intervalo')
                        socketio.emit('intervalo', {'t_on': inter.t_on, 't_off':inter.t_off, 'repetir': inter.repetir, 'stsInter': stsInter}, namespace='/test')
        
            
@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')
    # Start the timer thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(timeReleInter(None))


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
    return retornastatus()

def desativaTempo():
    global thread
    global thread_stop_event

    if not thread.isAlive():
        print("Stopping Thread")
        thread_stop_event = Event()

def ativaPorTempo():
    global webraspio_global
    global thread

    webraspio_global['statusSaida1'] = RpiGpio.ativa()
    webraspio_global['stsTempo'] = "ativado"

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(timeRele)

def ativaIntervalo(inter):
    global webraspio_global
    global thread

    webraspio_global['stsIntervalo'] = "ativado"
    webraspio_global['inter'] = True

    # Start the random number generator thread only if the thread has not been started before.
    # if not thread.isAlive():
    #     print("Starting Thread")
    #     thread = socketio.start_background_task(timeReleInter(inter))
