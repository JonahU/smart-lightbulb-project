import sounddevice
import numpy


def print_sound(indata, outdata, frames, time, status):
    '''
    SOURCE:
    https://stackoverflow.com/questions/40138031/how-to-read-realtime-microphone-audio-volume-in-python-and-ffmpeg-or-similar
    '''
    volume_norm = numpy.linalg.norm(indata)*10
    print("|" * int(volume_norm))


def start_sound(duration=10):
    with sounddevice.Stream(callback=print_sound):
        sounddevice.sleep(duration * 1000)


if __name__ == "__main__":
    start_sound()
