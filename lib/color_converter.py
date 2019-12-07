import colorsys

def to_rgb(hue, saturation, brightness, kelvin=None):
    hue = int(hue)/65535
    lightness = int(brightness)/65535
    saturation = int(saturation)/65535
    r,g,b = colorsys.hls_to_rgb(hue, lightness, saturation)
    r = int(r*100)
    g = int(g*100)
    b = int(b*100)
    if kelvin is not None:
        return {'r': r, 'g': g, 'b': b, 'kelvin': kelvin}
    else:
        return {'r': r, 'g': g, 'b': b}

def from_rgb(r, g, b, kelvin=None):
    r = int(r)/100
    g = int(g)/100
    b = int(b)/100
    h,l,s = colorsys.rgb_to_hls(r, g, b)
    h = int(h*65535)
    s = int(s*65535)
    l = int(l*65535)
    if kelvin is not None:
        return (h, s, l, kelvin)
    else:
        return (h, s, l)