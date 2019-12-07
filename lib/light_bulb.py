from lifxlan import Light
from dotenv import load_dotenv
from os import environ

import color_converter

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

    def get_color_rgb(self):
        h,s,b,k = self.get_color()
        rgbk = color_converter.to_rgb(h, s, b, kelvin=k)
        return rgbk

    def set_color_rgb(self, rgbk):
        r,g,b,k = rgbk
        hsbk = color_converter.from_rgb(r, g, b, kelvin=k)
        super().set_color(hsbk)