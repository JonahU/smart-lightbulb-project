# Utils
from os import environ
from dotenv import load_dotenv

# Core
from frontend.color_picker import start_frontend
from light_bulb import LightBulb

# Exception handling
from lifxlan import WorkflowException
from socket import gaierror


def main():
    load_dotenv()
    try:
        with LightBulb(environ['LIGHT_MAC'], environ['LIGHT_IP']) as my_bulb:
            start_frontend(my_bulb, environ['HOST'], environ['PORT'])
    except gaierror as err:
        print(
            'Invalid LIGHT_IP environment variable value:',
            f'"{environ["LIGHT_IP"]}"',
            "\nTo check your bulb's IP address",
            "please run the utils/find_lights.py script"
        )
    except WorkflowException as err:
        print(
            'Unable to connect to bulb with address:',
            f'"{environ["LIGHT_MAC"]}"',
            '\nPlease verify the bulb is connected to power',
            'and that your environment variables are set correctly',
            "\nTo check your bulb's MAC address",
            "please run the utils/find_lights.py script"
        )


if __name__ == '__main__':
    main()
