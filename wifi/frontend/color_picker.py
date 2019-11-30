from flask import Flask, request, render_template

flask_frontend = Flask(__name__)

@flask_frontend.route('/', methods=['GET','POST'])
def color_sliders_hsbk():
    if request.method == "POST":
        hsbk_color = request.form # hue, saturation, brightness, kelvin
        hue = int(hsbk_color['hue'])/65535
        saturation = int(hsbk_color['saturation'])/65535
        brightness = int(hsbk_color['brightness'])/65535
        kelvin = int(hsbk_color['kelvin'])

        print(hsbk_color)
    return render_template("color_picker.html")

if __name__ == '__main__':
   flask_frontend.run(debug=True)