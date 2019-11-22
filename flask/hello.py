from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def slider():
    if request.method == "POST":
        points = request.form['points']
        print(points)
    # points = request.args.get('points')
    return render_template("slider.html")

if __name__ == '__main__':
   app.run(debug=True)