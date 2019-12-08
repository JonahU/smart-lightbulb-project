from frontend.color_picker import start_frontend
from light_bulb import LightBulb
from os import environ

if __name__ == '__main__':
    with LightBulb() as my_bulb:
        start_frontend(my_bulb, environ['HOST'], environ['PORT'])
