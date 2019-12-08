# Utils
from os import environ
from dotenv import load_dotenv

# Core
from frontend.color_picker import start_frontend
from light_bulb import LightBulb


if __name__ == '__main__':
    load_dotenv()
    with LightBulb(environ['LIGHT_MAC'], environ['LIGHT_IP']) as my_bulb:
        start_frontend(my_bulb, environ['HOST'], environ['PORT'])
