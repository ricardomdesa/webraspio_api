from unittest.mock import Mock


class Gpio:

    def __init__(self, env: str):
        self._pin = 12
        if env == "rpi":
            import RPi.GPIO as GPIO
            self._gpio = GPIO
        else:
            self._gpio = Mock()
        self._gpio.setmode(self._gpio.BOARD)
        self._gpio.setup(self._pin, self._gpio.OUT)
        
        self._gpio.output(self._pin, True)

    def ativa(self):
        self._gpio.output(self._pin, False)
        return {"status rele", 'on'}

    def desativa(self):
        self._gpio.output(self._pin, True)
        return {"status rele", 'off'}
