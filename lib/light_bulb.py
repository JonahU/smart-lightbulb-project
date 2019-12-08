from lifxlan import Light, WorkflowException
import sounddevice
import numpy
from random import randint
import color_converter


class LightBulb(Light):
    MIN_HUE = 0
    MAX_HUE = 65535
    MIN_BRIGHTNESS = 0
    MAX_BRIGHTNESS = 65535
    MIN_SATURATION = 0
    MAX_SATURATION = 65535
    MIN_KELVIN = 2500
    MAX_KELVIN = 9000
    MIN_R = 0
    MAX_R = 100
    MIN_G = 0
    MAX_G = 100
    MIN_B = 0
    MAX_B = 100

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

    def start_listening(self, duration=10):
        super().set_color(LightBulb.hsbk_min())  # Dim bulb at start
        prev_volume = 0

        def sound_volume(indata, outdata, frames, time, status):
            nonlocal prev_volume
            volume = numpy.linalg.norm(indata)
            if volume > 2 and volume > 2*prev_volume:
                # Volume is increasing, light up bulb
                if volume < 5:
                    color = LightBulb.hsbk_max(
                        saturation=self.MIN_SATURATION,
                        brightness=15000)
                elif volume < 10:
                    color = LightBulb.hsbk_max(
                        saturation=self.MIN_SATURATION,
                        brightness=30000)
                elif volume < 20:
                    color = LightBulb.hsbk_max(
                        saturation=self.MIN_SATURATION,
                        brightness=45000)
                else:
                    color = LightBulb.hsbk_max(
                        saturation=self.MIN_SATURATION,
                        brightness=self.MAX_BRIGHTNESS)

                try:
                    self.set_color(color, rapid=True)
                except WorkFlowException:
                    # Occurs occasionally when changing colors quickly
                    pass
            elif volume < 1 or volume < 2 and 2*volume < prev_volume:
                # Volume is declining, dim bulb
                try:
                    self.set_color(LightBulb.hsbk_min(), duration=10)
                except WorkflowException:
                    # Occurs occasionally when changing colors quickly
                    pass
            prev_volume = volume

        # Call sound_volume for duration in seconds
        with sounddevice.Stream(callback=sound_volume):
            sounddevice.sleep(duration * 1000)

    @staticmethod
    def hsbk_min(
            hue=MIN_HUE,
            saturation=MIN_SATURATION,
            brightness=MIN_BRIGHTNESS,
            kelvin=MIN_KELVIN):
        return (hue, saturation, brightness, kelvin)

    @staticmethod
    def hsbk_max(
            hue=MAX_HUE,
            saturation=MAX_SATURATION,
            brightness=MAX_BRIGHTNESS,
            kelvin=MAX_KELVIN):
        return (hue, saturation, brightness, kelvin)

    def randomize(self):
        random = (
            randint(self.MIN_HUE, self.MAX_HUE),
            randint(self.MIN_SATURATION, self.MAX_HUE),
            randint(self.MIN_BRIGHTNESS, self.MAX_BRIGHTNESS),
            randint(self.MIN_KELVIN, self.MAX_KELVIN),
        )
        super().set_color(random)

    def flicker(self):
        try:
            super().set_waveform(1, LightBulb.hsbk_min(), 1000, 10, 0, 3)
        except WorkflowException:
            # Occurs occasionally when changing colors quickly
            pass
