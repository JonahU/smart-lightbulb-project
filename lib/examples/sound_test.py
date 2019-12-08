import sounddevice
import numpy

'''
SOURCE:
https://stackoverflow.com/questions/40138031/how-to-read-realtime-microphone-audio-volume-in-python-and-ffmpeg-or-similar
'''


def print_sound(indata, outdata, frames, time, status):
    volume_norm = numpy.linalg.norm(indata)*10
    print("|" * int(volume_norm))


def start_sound(duration=10):
    with sounddevice.Stream(callback=print_sound):
        sounddevice.sleep(duration * 1000)


def main():
    start_sound()


if __name__ == "__main__":
    main()