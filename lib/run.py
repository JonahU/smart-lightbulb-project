# Utils
from os import environ, path as ospath
from sys import path as syspath
from dotenv import load_dotenv

# Add frontend to path
lib_directory = ospath.dirname(__file__)
syspath.append(f'{lib_directory}{ospath.sep}frontend')

# Core
from frontend.app import start_frontend  # noqa: E402
from light_bulb import LightBulb         # noqa: E402

# Exception handling
from lifxlan import WorkflowException    # noqa: E402
from socket import gaierror              # noqa: E402


def main():
    load_dotenv()
    try:
        with LightBulb(environ['LIGHT_MAC'], environ['LIGHT_IP']) as my_bulb:
            start_frontend(my_bulb, environ['HOST'], environ['PORT'])
    except gaierror:
        print(
            'Invalid LIGHT_IP environment variable value:',
            f'"{environ["LIGHT_IP"]}"',
            "\nTo check your bulb's IP address",
            "please run the utils/find_lights.py script"
        )
    except WorkflowException:
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
