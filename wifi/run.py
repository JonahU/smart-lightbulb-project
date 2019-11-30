from frontend.color_picker import flask_frontend
from setup import setup

if __name__ == '__main__':
    setup()
    flask_frontend.run(debug=True)