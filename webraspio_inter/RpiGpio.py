import RPi.GPIO as GPIO #teste no pc



# pinSaida1 = 11;
pinSaida1 = 40;
# pinSaida2 = 12;



def inicia():
    print('inicia Gpio')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pinSaida1, GPIO.OUT)
    
    GPIO.output(pinSaida1, True)

def ativa():
    GPIO.output(pinSaida1, False)
    # print('rele 1 ativado')
    return 'on'

def desativa():
    GPIO.output(pinSaida1, True)
    # print('rele 1 desativado')
    return 'off'
