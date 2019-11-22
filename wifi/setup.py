
from lifxlan import LifxLAN, Light
from dotenv import load_dotenv
from os import environ

load_dotenv()

lan = LifxLAN()
lights = Light(environ['LIGHT_MAC'], environ['LIGHT_IP'])
