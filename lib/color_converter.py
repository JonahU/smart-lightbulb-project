import colorsys

def to_rgb(hue, saturation, brightness):
    hue = int(hue)/65535
    lightness = int(brightness)/65535
    saturation = int(saturation)/65535
    r,g,b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return {'red': r, 'green': g, 'blue': b}