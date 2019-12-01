
from lifxlan import LifxLAN, Light
from dotenv import load_dotenv
from os import environ

def setup():
    # General setup
    load_dotenv()

    # Bulb setup
    lan = LifxLAN()
    my_bulb = Light(environ['LIGHT_MAC'], environ['LIGHT_IP'])

    # Turn on bulb if it is off
    my_bulb.set_power(1, 3000) # 3 second transition

    my_bulb.set_color([65535,65535,65535,9000])
    my_bulb.set_brightness(65535)
    my_bulb.set_saturation(65535)

    return my_bulb
