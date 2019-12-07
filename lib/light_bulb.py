from lifxlan import Light
from dotenv import load_dotenv
from os import environ

class LightBulb(Light):
    def __init__(self):
        # General setup
        load_dotenv()

        # Bulb setup
        super().__init__(environ['LIGHT_MAC'], environ['LIGHT_IP'])

    def __enter__(self):
        # Turn on bulb with 3 second transition
        self.set_power(1, 3000)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.set_power(0) # Turn off bulb