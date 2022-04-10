from unittest.mock import Mock


class TemperatureSensor:
    def __init__(self, env: str):
        self.temp_json = {'temp': 0.0}
        if env == "rpi":
            import Adafruit_BMP.BMP085 as BMP085
            self.sensor = BMP085.BMP085()
        else:
            self.sensor = Mock()

    def get_temperature(self):
        self.temp_json['temp'] = '{0:0.2f}'.format(self.sensor.read_temperature())
        return self.temp_json
