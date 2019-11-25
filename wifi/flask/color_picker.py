from flask import Flask, request, render_template
from color_converter import to_rgb

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def slider():
    if request.method == "POST":
        hsbk_color = request.form # hue, saturation, brightness, kelvin
        hue = int(hsbk_color['hue'])/65535
        saturation = int(hsbk_color['saturation'])/65535
        brightness = int(hsbk_color['brightness'])/65535
        kelvin = int(hsbk_color['kelvin'])
        rgb_color = to_rgb(hue, brightness, saturation)

        print(hsbk_color)
        print(rgb_color)
    return render_template("color_picker.html")

if __name__ == '__main__':
   app.run(debug=True)