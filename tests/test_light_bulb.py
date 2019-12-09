import pytest
from os import environ, path as ospath
from sys import path as syspath
from pathlib import Path
from dotenv import load_dotenv


# Add lib to path
root_dir = Path(ospath.dirname(__file__)).parent
lib_dir = f'{root_dir}{ospath.sep}lib'
syspath.append(lib_dir)

MIN_HUE = 0
MIN_BRIGHTNESS = 0
MIN_SATURATION = 0
MIN_KELVIN = 2500
MIN_R = 0
MIN_G = 0
MIN_B = 0

MAX_HUE = 65535
MAX_BRIGHTNESS = 65535
MAX_SATURATION = 65535
MAX_KELVIN = 9000
MAX_R = 100
MAX_G = 100
MAX_B = 100

from lib import light_bulb   # noqa: E402
from socket import gaierror  # noqa: E402
load_dotenv()

bulb = None
no_connection = True
try:
    with light_bulb.LightBulb(
            environ['LIGHT_MAC'],
            environ['LIGHT_IP']) as bulb:
        no_connection = False
except (light_bulb.WorkflowException, gaierror):
    no_connection = True


@pytest.fixture
def light_bulb_connection():
    return bulb


@pytest.fixture
def light_bulb_object():
    from lib import light_bulb
    return light_bulb.LightBulb


@pytest.mark.skipif(no_connection, reason="no connection")
def test_get_color(light_bulb_connection):
    color = light_bulb_connection.get_color()

    assert type(color) == tuple
    assert len(color) == 4
    assert MIN_HUE <= color[0] <= MAX_HUE
    assert MIN_BRIGHTNESS <= color[1] <= MAX_BRIGHTNESS
    assert MIN_SATURATION <= color[2] <= MAX_SATURATION
    assert MIN_KELVIN <= color[3] <= MAX_KELVIN


@pytest.mark.skipif(no_connection, reason="no connection")
def test_get_color_rgb(light_bulb_connection):
    color = light_bulb_connection.get_color_rgb()

    assert type(color) == tuple
    assert len(color) == 4
    assert MIN_R <= color[0] <= MAX_R
    assert MIN_G <= color[1] <= MAX_G
    assert MIN_B <= color[2] <= MAX_B
    assert MIN_KELVIN <= color[3] <= MAX_KELVIN


@pytest.mark.skipif(no_connection, reason="no connection")
def test_set_color_rgb_min(light_bulb_connection):
    rgbk = (0, 0, 0, 2500)
    light_bulb_connection.set_color_rgb(rgbk)
    color = light_bulb_connection.get_color()

    assert color[0] == MIN_HUE
    assert color[1] == MIN_BRIGHTNESS
    assert color[2] == MIN_SATURATION
    assert color[3] == MIN_KELVIN


@pytest.mark.skipif(no_connection, reason="no connection")
def test_set_color_rgb_max(light_bulb_connection):
    rgbk = (100, 100, 100, 9000)
    light_bulb_connection.set_color_rgb(rgbk)
    color = light_bulb_connection.get_color()

    assert color[0] == MIN_HUE
    assert color[1] == MIN_BRIGHTNESS
    assert color[2] == MAX_SATURATION
    assert color[3] == MAX_KELVIN


@pytest.mark.skipif(no_connection, reason="no connection")
@pytest.mark.skip(reason="causes set_color_rgb_min to behave strangely")
def test_randomize(light_bulb_connection):
    before = light_bulb_connection.get_color()
    light_bulb_connection.randomize()
    after = light_bulb_connection.get_color()
    assert before != after


def test_rgbk_min(light_bulb_object):
    color = light_bulb_object.rgbk_min()
    assert type(color) == tuple
    assert len(color) == 4
    assert color[0] == MIN_R
    assert color[1] == MIN_G
    assert color[2] == MIN_B
    assert color[3] == MIN_KELVIN


def test_rgbk_max(light_bulb_object):
    color = light_bulb_object.rgbk_max()
    assert type(color) == tuple
    assert len(color) == 4
    assert color[0] == MAX_R
    assert color[1] == MAX_G
    assert color[2] == MAX_B
    assert color[3] == MAX_KELVIN


def test_hsbk_min(light_bulb_object):
    color = light_bulb_object.hsbk_min()
    assert type(color) == tuple
    assert len(color) == 4
    assert color[0] == MIN_HUE
    assert color[1] == MIN_SATURATION
    assert color[2] == MIN_BRIGHTNESS
    assert color[3] == MIN_KELVIN


def test_hsbk_max(light_bulb_object):
    color = light_bulb_object.hsbk_max()
    assert type(color) == tuple
    assert len(color) == 4
    assert color[0] == MAX_HUE
    assert color[1] == MAX_SATURATION
    assert color[2] == MAX_BRIGHTNESS
    assert color[3] == MAX_KELVIN
