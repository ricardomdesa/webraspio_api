from fastapi import FastAPI
from rpi_gpio import Gpio
from settings import get_settings


app = FastAPI()
settings = get_settings()

gpio = Gpio(env = settings.ENV)

@app.get("/health")
def health():
    return {"status": "OK"}


@app.post("/on/")
def turn_on():
    breakpoint()
    return gpio.ativa()
