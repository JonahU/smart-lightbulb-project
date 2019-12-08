from lifxlan import Light, WorkflowException
import sounddevice
import numpy
from random import randint
import color_converter


class LightBulb(Light):
    '''
    A class to control LIFX smart color bulbs
    This class extends the functionality of lifxlan's Light class
    The color of the bulb is stored in HSBK format
    HSBK = Hue, Saturation, Brightness, Kelvin

    ...

    Important Inherited Methods
    -------
    __init__(mac_address, ip_address)
        LightBulb constructor
    get_color():
        Returns the color of the bulb in HSBK format
    set_color(hsbk)
        Set the color of the bulb with HSBK formatted list/tuple

    Instance Methods
    -------
    get_color_rgb()
        Returns the color of the bulb in RGB + kelvin format
    set_color_rgb(rgbk)
        Sets the color of the bulb with RGB + kelvin formatted list/tuple
    start_listening(duration=10)
        Listen to the hardware microphone for duration period
        Increase light brightness depending on loudness of input
    randomize()
        Sets the bulb's color to a random color
    flicker(duration=10)
        Flicker the bulb for duration period

    Static Methods
    -------
    hsbk_min(hue=MIN_HUE,
            saturation=MIN_SATURATION,
            brightness=MIN_BRIGHTNESS,
            kelvin=MIN_KELVIN)
        Returns a min values color tuple in HSBK format
    hsbk_max(
            hue=MAX_HUE,
            saturation=MAX_SATURATION,
            brightness=MAX_BRIGHTNESS,
            kelvin=MAX_KELVIN)
        Returns a max values color tuple in HSBK format
    rgbk_min(
            r=MIN_R,
            g=MIN_G,
            b=MIN_B,
            kelvin=MIN_KELVIN)
        Returns a min values color tuple in RGB + kelvin format
    rgbp_max(
            r=MAX_R,
            g=MAX_G,
            b=MAX_B,
            kelvin=MAX_KELVIN)
        Returns a max values color tuple in RGB + kelvin format
    '''

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
        '''Turn on bulb with 3 second transition'''
        self.set_power(1, 3000)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        '''Turn off bulb'''
        self.set_power(0)

    def get_color_rgb(self):
        '''Return color in RGB + kelvin format'''
        h, s, b, k = self.get_color()
        rgbk = color_converter.to_rgb(h, s, b, kelvin=k)
        return rgbk

    def set_color_rgb(self, rgbk):
        '''Set the color of the bulb to the specified RGB + kelvin values'''
        r, g, b, k = rgbk
        hsbk = color_converter.from_rgb(r, g, b, kelvin=k)
        super().set_color(hsbk)

    def start_listening(self, duration=10):
        '''
        Listen to the built-in microphone for the specified time period,
        increase the bulb's brightness upon loud of input
        '''
        super().set_color(LightBulb.hsbk_min())  # Dim bulb at start
        prev_volume = 0

        def sound_volume(indata, outdata, frames, time, status):
            '''
            Callback for sounddevice.Stream, if the difference
            between current volume and previous volume
            is high enough, changes the bulb's brightness
            '''
            nonlocal prev_volume
            volume = numpy.linalg.norm(indata)  # Normalize sound data
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
                # Volume is too low or decreasing, dim bulb
                try:
                    # Reduce brightness with 10 millisecond smooth transition
                    self.set_color(LightBulb.hsbk_min(), duration=10)
                except WorkflowException:
                    # Occurs occasionally when changing colors quickly
                    pass
            prev_volume = volume

        # Call sound_volume for duration in seconds
        with sounddevice.Stream(callback=sound_volume):
            sounddevice.sleep(duration * 1000)

    def randomize(self):
        '''Set the bulb's color to a random color'''
        random = (
            randint(self.MIN_HUE, self.MAX_HUE),
            randint(self.MIN_SATURATION, self.MAX_HUE),
            randint(self.MIN_BRIGHTNESS, self.MAX_BRIGHTNESS),
            randint(self.MIN_KELVIN, self.MAX_KELVIN),
        )
        super().set_color(random)

    def flicker(self, duration=10):
        '''Set the bulb to flicker the specified time period'''
        period = duration*100
        cycles = duration
        try:
            super().set_waveform(1, LightBulb.hsbk_min(), period, cycles, 0, 3)
        except WorkflowException:
            # Occurs occasionally when changing colors quickly
            pass

    @staticmethod
    def hsbk_min(
            hue=MIN_HUE,
            saturation=MIN_SATURATION,
            brightness=MIN_BRIGHTNESS,
            kelvin=MIN_KELVIN):
        '''Returns a min values color tuple in HSBK format'''
        return (hue, saturation, brightness, kelvin)

    @staticmethod
    def hsbk_max(
            hue=MAX_HUE,
            saturation=MAX_SATURATION,
            brightness=MAX_BRIGHTNESS,
            kelvin=MAX_KELVIN):
        '''Returns a max values color tuple in HSBK format'''
        return (hue, saturation, brightness, kelvin)

    @staticmethod
    def rgbk_min(
            r=MIN_R,
            g=MIN_G,
            b=MIN_B,
            kelvin=MIN_KELVIN):
        '''Returns a min values color tuple in RGB + kelvin format'''
        return (r, g, b, kelvin)

    @staticmethod
    def rgbp_max(
            r=MAX_R,
            g=MAX_G,
            b=MAX_B,
            kelvin=MAX_KELVIN):
        '''Returns a max values color tuple in RGB + kelvin format'''
        return (r, g, b, kelvin)
