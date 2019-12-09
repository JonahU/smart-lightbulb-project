import pytest
from lib import color_converter

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


def test_to_rgb():
    hue = '24000'
    brightness = '54000'
    saturation = '2100'
    after = color_converter.to_rgb(hue, saturation, brightness)

    assert type(after) == tuple
    assert len(after) == 3
    assert 0 < after[0] < 100
    assert 0 < after[1] < 100
    assert 0 < after[2] < 100


def test_to_rgb_min():
    hue = str(MIN_HUE)
    brightness = str(MIN_BRIGHTNESS)
    saturation = str(MIN_SATURATION)
    kelvin = str(MIN_KELVIN)
    after = color_converter.to_rgb(hue, saturation, brightness, kelvin=kelvin)

    assert type(after) == tuple
    assert len(after) == 4
    assert after[0] == MIN_R
    assert after[1] == MIN_G
    assert after[2] == MIN_B
    assert after[3] == kelvin


def test_to_rgb_max():
    hue = str(MAX_HUE)
    brightness = str(MAX_BRIGHTNESS)
    saturation = str(MAX_SATURATION)
    kelvin = str(MAX_KELVIN)
    after = color_converter.to_rgb(hue, saturation, brightness, kelvin=kelvin)

    assert type(after) == tuple
    assert len(after) == 4
    assert after[0] == MAX_R
    assert after[1] == MAX_G
    assert after[2] == MAX_B
    assert after[3] == kelvin


def test_from_rgb():
    r = '82'
    g = '21'
    b = '1'
    after = color_converter.from_rgb(r, g, b)

    assert type(after) == tuple
    assert len(after) == 3
    assert 0 < after[0] < 65535
    assert 0 < after[1] < 65535
    assert 0 < after[2] < 65535


def test_from_rgb_min():
    r = MIN_R
    g = MIN_G
    b = MIN_B
    kelvin = MIN_KELVIN
    after = color_converter.from_rgb(r, g, b, kelvin=kelvin)

    assert type(after) == tuple
    assert len(after) == 4
    assert after[0] == MIN_HUE
    assert after[1] == MIN_SATURATION
    assert after[2] == MIN_BRIGHTNESS
    assert after[3] == kelvin


def test_from_rgb_max():
    r = MAX_R
    g = MAX_G
    b = MAX_B
    kelvin = MAX_KELVIN
    after = color_converter.from_rgb(r, g, b, kelvin=kelvin)

    assert type(after) == tuple
    assert len(after) == 4
    assert after[0] == MIN_HUE
    assert after[1] == MIN_SATURATION
    assert after[2] == MAX_BRIGHTNESS
    assert after[3] == kelvin
