from fastapi import FastAPI
from rpi_gpio import Gpio
from settings import get_settings
from src.temperature_sensor import TemperatureSensor

app = FastAPI()
settings = get_settings()

gpio = Gpio(env=settings.ENV)
temp_sensor = TemperatureSensor(env=settings.ENV)


@app.get("/health")
def health():
    return {"status": "OK"}


@app.post("/on/")
def turn_on():
    return gpio.ativa()


@app.post("/off/")
def turn_off():
    return gpio.desativa()


@app.get("/temp")
def get_temp():
    return temp_sensor.get_temperature()
