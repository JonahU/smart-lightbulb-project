from flask import Flask, request, render_template, after_this_request

flask_frontend = Flask(__name__)
my_bulb = None

def handle_color_change(new_values):
    if my_bulb is not None:
        if hue in new_values: # hsbk
            my_bulb.set_color(list(new_values))
        else: # rgb
            raise NotImplementedError
    else:
        print(new_values)

@flask_frontend.route('/', methods=['GET'])
def root():
    return render_template("index.html")

@flask_frontend.route('/hsbk', methods=['GET','POST'])
def color_sliders_hsbk():
    if request.method == "POST":
        hsbk_color = request.form # hue, saturation, brightness, kelvin
        handle_color_change(hsbk_color)
        return render_template("hsbk_color_picker.html", form=hsbk_color)
    elif request.method == "GET":
        default_form = {
            "hue": 0,
            "brightness": 0,
            "saturation": 0,
            "kelvin": 2500
        }
        return render_template("hsbk_color_picker.html", form=default_form)

@flask_frontend.route('/rgb', methods=['GET','POST'])
def color_sliders_rgb():
    if request.method == "POST":
        rgb_color = request.form
        handle_color_change(rgb_color)
        return render_template("rgb_color_picker.html", form=rgb_color)
    elif request.method == "GET":
        default_form = {
            "r": 0,
            "g": 0,
            "b": 0,
            "kelvin": 2500
        }
        return render_template("rgb_color_picker.html", form=default_form)

def start_frontend(lightbulb):
    global my_bulb
    my_bulb = lightbulb
    flask_frontend.run(debug=True)

if __name__ == '__main__':
   flask_frontend.run(debug=True)