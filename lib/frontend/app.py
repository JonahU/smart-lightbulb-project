'''
This module defines four routes:
    /               -   Homepage
    /hsbk           -   HSBK color picker
    /rgb            -   RGB color picker
    /experiments    -   Experiments page

HTML files for the different routes are located in the templates folder

HOW TO RUN:
    1) This module can be executed directly from the command line for
        testing purposes
    2) This module can be run from another python file with function
        start_frontend(lightbulb, host=localhost, port=5000)

KNOWN ISSUES:
    1) On the experiments page, repeated pressing of the "Sound Experiment"
        button before the timer has finished counting down leads to
        unpredictable behavior and may cause the entire program to crash.
    2) Some scaling issues with narrow windows may lead to overlapping text.
'''

from flask import Flask, request, render_template, after_this_request
from handler import (
    handle_color_change,
    handle_flicker,
    handle_randomize,
    handle_start_listening)

flask_frontend = Flask(__name__)
my_bulb = None


@flask_frontend.route('/', methods=['GET'])
def root():
    return render_template("index.html")


@flask_frontend.route('/hsbk', methods=['GET', 'POST'])
def color_sliders_hsbk():
    if request.method == "POST":
        hsbk_color = request.form  # hue, saturation, brightness, kelvin
        handle_color_change(my_bulb, hsbk_color)
        return render_template("hsbk_color_picker.html", form=hsbk_color)
    elif request.method == "GET":
        if my_bulb is not None:
            prev_values = my_bulb.get_color()
            initial = {
                "hue": prev_values[0],
                "brightness": prev_values[1],
                "saturation": prev_values[2],
                "kelvin": prev_values[3]
            }
        else:
            initial = {
                "hue": 0,
                "brightness": 0,
                "saturation": 0,
                "kelvin": 2500
            }
        return render_template("hsbk_color_picker.html", form=initial)


@flask_frontend.route('/rgb', methods=['GET', 'POST'])
def color_sliders_rgb():
    if request.method == "POST":
        rgb_color = request.form
        handle_color_change(my_bulb, rgb_color)
        return render_template("rgb_color_picker.html", form=rgb_color)
    elif request.method == "GET":
        if my_bulb is not None:
            prev_values = my_bulb.get_color_rgb()
            initial = prev_values
        else:
            initial = {
                "r": 0,
                "g": 0,
                "b": 0,
                "kelvin": 2500
            }
        return render_template("rgb_color_picker.html", form=initial)


@flask_frontend.route('/experiments', methods=['GET', 'POST'])
def experiments():
    if request.method == "POST":
        if "sound-experiment" in request.form:
            # Sound experiment button was pressed
            handle_start_listening(my_bulb)
        elif "randomize-experiment" in request.form:
            handle_randomize(my_bulb)
        elif "flicker-experiment" in request.form:
            handle_flicker(my_bulb)
        return render_template("experiments.html")
    elif request.method == "GET":
        return render_template("experiments.html")


def start_frontend(lightbulb, host="localhost", port=5000):
    global my_bulb
    my_bulb = lightbulb
    flask_frontend.run(host=host, port=port)


if __name__ == '__main__':
    flask_frontend.run(debug=True)
