from lifxlan import Light, WorkflowException
import sounddevice
import numpy
import color_converter


class LightBulb(Light):
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
                    color = LightBulb.hsbk_max(saturation=0, brightness=15000)
                elif volume < 10:
                    color = LightBulb.hsbk_max(saturation=0, brightness=30000)
                elif volume < 20:
                    color = LightBulb.hsbk_max(saturation=0, brightness=45000)
                else:
                    color = LightBulb.hsbk_max(saturation=0, brightness=65535)

                try:
                    self.set_color(color, rapid=True)
                except WorkFlowException as e:
                    # Occurs very occasionally when rapid is enabled
                    pass
            elif volume < 1 or volume < 2 and 2*volume < prev_volume:
                # Volume is declining, dim bulb
                self.set_color(LightBulb.hsbk_min(), duration=10)
            prev_volume = volume
        with sounddevice.Stream(callback=sound_volume):
            sounddevice.sleep(duration * 1000)

    @staticmethod
    def hsbk_min(hue=0, saturation=0, brightness=0, kelvin=2500):
        return (hue, saturation, brightness, kelvin)

    @staticmethod
    def hsbk_max(hue=65535, saturation=65535, brightness=65535, kelvin=9000):
        return (hue, saturation, brightness, kelvin)
