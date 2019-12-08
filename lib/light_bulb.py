# General program setup
from dotenv import load_dotenv
from os import environ

# Lightbulb utils
from lifxlan import Light
import sounddevice
import numpy
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
        self.set_power(0)  # Turn off bulb

    def get_color_rgb(self):
        h, s, b, k = self.get_color()
        rgbk = color_converter.to_rgb(h, s, b, kelvin=k)
        return rgbk

    def set_color_rgb(self, rgbk):
        r, g, b, k = rgbk
        hsbk = color_converter.from_rgb(r, g, b, kelvin=k)
        super().set_color(hsbk)

    def _sound_volume(self, indata, outdata, frames, time, status):
        '''
        SOURCE:
        https://stackoverflow.com/questions/40138031/how-to-read-realtime-microphone-audio-volume-in-python-and-ffmpeg-or-similar
        '''
        volume_norm = numpy.linalg.norm(indata)*10
        super().set_brightness(volume_norm)

    def start_listening(self, duration=10):
        with sounddevice.Stream(callback=self._sound_volume):
            sounddevice.sleep(duration * 1000)
