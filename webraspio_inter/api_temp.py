from flask import Flask, render_template, jsonify

import Adafruit_BMP.BMP085 as BMP085

app = Flask(__name__)

temp_json = {
    'temp': 0.0
}

sensor = BMP085.BMP085()

@app.route('/')
def index():
    temp="There I'll put instructions..."
    return render_template("index.php", temp=temp)


@app.route('/api/temp', methods=['GET'])
def api_all():
    global temp_json
    temp_json['temp'] = '{0:0.2f}'.format(sensor.read_temperature())

    return jsonify(temp_json)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
