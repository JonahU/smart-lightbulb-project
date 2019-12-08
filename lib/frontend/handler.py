def handle_color_change(my_bulb, new_values):
    if my_bulb is not None:
        if "hue" in new_values:  # hsbk
            new_color = (
                new_values['hue'],
                new_values['saturation'],
                new_values['brightness'],
                new_values['kelvin']
            )
            my_bulb.set_color(new_color)
        else:  # rgb
            new_color = (
                new_values['r'],
                new_values['g'],
                new_values['b'],
                new_values['kelvin'],
            )
            my_bulb.set_color_rgb(new_color)
    else:
        print(f"New color: {new_values}")


def handle_flicker(my_bulb):
    if my_bulb is not None:
        my_bulb.flicker()
    else:
        print("Flickering bulb for 10 seconds")


def handle_start_listening(my_bulb):
    if my_bulb is not None:
        my_bulb.start_listening(duration=20)
    else:
        print("Responding to mic input for 20 seconds")


def handle_randomize(my_bulb):
    if my_bulb is not None:
        my_bulb.randomize()
    else:
        print("Setting bulb to random color")
