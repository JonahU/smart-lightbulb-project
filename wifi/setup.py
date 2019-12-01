
from lifxlan import LifxLAN, Light
from dotenv import load_dotenv
from os import environ

class setup_bulb():
    def __init__(self):
        # General setup
        load_dotenv()

        # Bulb setup
        lan = LifxLAN()
        self.lightbulb = Light(environ['LIGHT_MAC'], environ['LIGHT_IP'])

    def __enter__(self):
        # Turn on bulb with 3 second transition
        self.lightbulb.set_power(1, 3000)
        return self.lightbulb

    def __exit__(self, exception_type, exception_value, traceback):
        self.lightbulb.set_power(0) # Turn off bulb
