from frontend.color_picker import start_frontend
from setup import setup_bulb
from os import environ

if __name__ == '__main__':
    with setup_bulb() as my_bulb:
        start_frontend(my_bulb, environ['HOST'], environ['PORT'])
