import pygatt
from binascii import hexlify

adapter = pygatt.BGAPIBackend()
MAC_ADDRESS = 'something'

def print_stuff(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

try:
    adapter.start()
    device = adapter.connect(MAC_ADDRESS)
    value = device.char_read("a1e8f5b1-696b-4e4c-87c6-69dfe0b0093b", callback=print_stuff)
finally:
    adapter.stop()