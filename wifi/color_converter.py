import colorsys

def to_rgb(hue, lightness, saturation):
    r,g,b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return {'red': r, 'green': g, 'blue': b}