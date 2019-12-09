import pytest
from light_bulb import LightBulb, WorkflowException


@pytest.fixture
def light_bulb():
    from os import environ
    from dotenv import load_dotenv
    load_dotenv()

    try:
        return LightBulb(environ['LIGHT_MAC'], environ['LIGHT_IP'])
    except WorkflowException as err:
        # print(err)
        raise err


def test_get_color(light_bulb):
    color = light_bulb.get_color()
    assert type(color) == tuple
