from flask import Flask

app = Flask(__name__)

webraspio_global = {'tempo' : 0,
                     'stsTempo': "desativado",
                     'stsIntervalo': "desativado", 
                     'statusSaida1': 'off', 
                     'horaInicio': 0,
                     'redir': {'redirect':''},
                     'inter': False,
                     'temp': None,
                     'setTemp': 27.0,
                     'tempEnabled': False,
                     'objInter':None}   

from views import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
