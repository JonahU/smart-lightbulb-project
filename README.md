# MPCS 51046 (Autumn 2019) Course Project - Jonah Usadi

## Overview - Smart light bulb library

This library provides functionality to interface with LIFX color smart light bulbs. The core of the library is the LightBulb class which can be found in the lib folder. This class extends the functionality of the Light class from [lifxlan](https://github.com/mclarkk/lifxlan). This library can be run directly with the provided lightweight web interface or imported within your own program. Some of the code in this library has been designed to work independently without a LIFX bulb (see 'other utils' below for more details). 

### Getting started

Set the `LIGHT_IP` and `LIGHT_MAC` environment variables in the `.env` file in the root of the project. If you are unsure of your light's ip and mac addresses, run the `utils/find_lights.py` script. Make sure your WiFi connection is 2.4GHz (this is the required frequency for connecting to LIFX devices).

Install the following dependencies:

- lifxlan
- sounddevice
- numpy
- python-dotenv (optional if importing LightBulb only)
- flask (optional if importing LightBulb only)
- pytest (if running tests)

Once all of the above is set up start the program by running `lib/run.py`. If all is working correctly you should now be able to go the provided link and control the smart bulb via the web interface.

### Tools used

- pytest is required to run tests. If a connection to a LIFX light bulb cannot be established, some of the tests will be skipped.
- pycodestyle is used for linting.

### My testing environment

I wrote and ran all of this code using using Python 3.7.x on a Windows machine. None of the code is platform specific and all of the libraries used claim multi-platform support. That being said, I have not tested this library on other machines or in other environments. Therefore, I cannot guarantee functionality on other operating systems/ all hardware. In particular, the `LightBulb.start_listening()` method might not work correctly as it involves interfacing with your hardware microphone (via the sounddevice library).

### Known issues

1) On the `/experiments` page, repeated pressing of the "Sound Experiment" button before the timer has finished counting down leads to unpredictable behavior and may cause the entire program to crash.
2) Frontend scaling issues, in particular narrow windows may lead to overlapping text.

### Other utils

The following are included with the library and can be run independent of a LIFX bulb:

- `utils/find_lights.py` - Detect and outputs all discoverable LIFX lights
- `utils/sound_test.py` - Using the same logic as `LightBulb.start_listening()`, picks up input from built-in microphone and outputs to console
- `lib/frontend/app.py` - Run the frontend without a LIFX bulb, outputs what would happen to the bulb to the console
