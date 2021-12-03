from web_socket import ativaIntervalo
class Intervalo():

    def __init__(self, t_off, t_on, repetir):
        self.t_off = t_off
        self.t_on = t_on
        self.repetir = repetir

    def start_intervalo(self):
        print('\n\n' + '=== Iniciando intervalo ===' + '\n\n')
        ativaIntervalo(self)
    
    def ligado(self):
        print('\n ===== inter ligado ===== \n')

    def desligado(self):
        print('\n ------ inter desligado ----- \n')