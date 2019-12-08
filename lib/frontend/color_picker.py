from flask import Flask, request, render_template, after_this_request

flask_frontend = Flask(__name__)
my_bulb = None


def handle_color_change(new_values):
    if my_bulb is not None:
        if "hue" in new_values:  # hsbk
            new_color = (
                new_values['hue'],
                new_values['saturation'],
                new_values['brightness'],
                new_values['kelvin']
            )
            my_bulb.set_color(new_color)
        else:  # rgb
            new_color = (
                new_values['r'],
                new_values['g'],
                new_values['b'],
                new_values['kelvin'],
            )
            my_bulb.set_color_rgb(new_color)
    else:
        print(new_values)


@flask_frontend.route('/', methods=['GET'])
def root():
    return render_template("index.html")


@flask_frontend.route('/hsbk', methods=['GET', 'POST'])
def color_sliders_hsbk():
    if request.method == "POST":
        hsbk_color = request.form  # hue, saturation, brightness, kelvin
        handle_color_change(hsbk_color)
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
        handle_color_change(rgb_color)
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
            my_bulb.start_listening(duration=20)
        elif "randomize-experiment" in request.form:
            my_bulb.randomize()
        elif "flicker-experiment" in request.form:
            my_bulb.flicker()
        return render_template("experiments.html")
    elif request.method == "GET":
        return render_template("experiments.html")


def start_frontend(lightbulb, host, port):
    global my_bulb
    my_bulb = lightbulb
    flask_frontend.run(debug=True, host=host, port=port)


if __name__ == '__main__':
    flask_frontend.run(debug=True)
