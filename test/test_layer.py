import re
import sangfroid
from test import *

def test_layer_children():
    sif = get_sif('pick-and-mix.sif')

    found = [re.search(r'([a-z]+)', str(layer))[0]
             for layer in sif.descendants]

    assert found==[
            "scale",
            "translate",
            "rotate",
            "timeloop",
            "stroboscope",
            "freetime",
            "shade",
            "bevel",
            "xor",
            "text",
            "switch",
            "super",
            "sound",
            "skeleton",
            "plant",
            "switch",
            "group",
            "filter",
            "duplicate",
            "spiral",
            "radial",
            "noise",
            "linear",
            "curve",
            "conical",
            "star",
            "solid",
            "region",
            "rectangle",
            "polygon",
            "outline",
            "outline",
            "circle",
            "checker",
            "advanced",
            "mandelbrot",
            "julia",
            "lumakey",
            "halftone",
            "halftone",
            "colorcorrect",
            "clamp",
            "chromakey",
            "simple",
            "metaballs",
            "warp",
            "twirl",
            "stretch",
            "spherize",
            "skeleton",
            "noise",
            "inside",
            "curve",
            "radial",
            "motion",
            "blur",
            ]

def test_layer_items():
    sif = get_sif('bouncing.sif')

    def format_value(v):
        result = f'{v.__class__.__name__}, {v}'
        if v.is_animated:
            result += ', animated'
        return result

    found = ''
    for layer in sif.descendants:
        found += f'{layer}\n'

        for k, v in layer.items():

            if isinstance(v, sangfroid.value.Composite):
                found += f' - {k}:\n'
                for k2, v2 in v.items():
                    found += f'     - {k2} = '+format_value(v2)+'\n'
            else:
                found += f' - {k}: '+format_value(v)+'\n'

    assert found == LAYER_ITEMS_EXPECTED

def _find_type_names_of_children_of_layer(layer):
    """
    Given a layer, returns a list of strings, each being the name of a
    layer which is a child of the parameter, in order; if a layer has
    no name, the member is None. The result is in the same order that
    the layers appear in the sif file.

    This gives a sort of signature for checking that the layers we find
    are the layers we expected to find.
    """
    result = [
            [
            b['type']
            for b in a
            ] for a in layers
            ]
    return result

def test_layer_find_all():
    sif = get_sif('bouncing.sif')
    shadows = sif.find_all(desc='Shadow')
    assert [x.desc for x in shadows] == ['Shadow', 'Shadow']

    circles = sif.find_all('circle')
    assert [x.desc for x in circles] == [
            'Shadow circle', 'Bouncy ball']

    wombats = sif.find_all('wombat')
    assert wombats == []

def test_layer_find():
    sif = get_sif('circles.sif')
    orange_circle = sif.find(desc='Orange circle')
    assert isinstance(orange_circle, sangfroid.layer.Layer)
    assert orange_circle.desc == 'Orange circle'

LAYER_ITEMS_EXPECTED = """
[🕰️timeloop]
 - z_depth: Real, 0.0
 - link_time: Time, 0f
 - local_time: Time, 0f
 - duration: Time, 48f
 - only_for_positive_duration: Bool, True
 - symmetrical: Bool, True
[📂group 'Ball']
 - z_depth: Real, 0.0
 - amount: Real, 0.75
 - blend_method: Integer, 13
 - origin: Vector, {'x': '0.0000000000', 'y': '0.0000000000'}
 - transformation:
     - offset = Vector, (animated), animated
     - angle = Angle, 0.0
     - skew_angle = Angle, 0.0
     - scale = Vector, (animated), animated
 - canvas: Canvas, [[-🔵circle 'Bouncy ball'], [-🫴bevel]]
 - color: Color, ff0000ff
 - radius: Real, 1.0
 - feather: Real, 0.0
 - invert: Bool, True
 - type: Integer, 1
 - color1: Color, ffffffff
 - color2: Color, 000000ff
 - angle: Angle, 89.058815
 - depth: Real, 0.5819661441
 - softness: Real, 0.3276240462
 - use_luma: Bool, True
 - solid: Bool, True
 - fake_origin: Vector, {'x': '0.0000000000', 'y': '0.0000000000'}
 - time_dilation: Real, 1.0
 - time_offset: Time, 0f
 - children_lock: Bool, True
 - outline_grow: Real, 0.0
 - z_range: Bool, True
 - z_range_position: Real, 0.0
 - z_range_depth: Real, 0.0
 - z_range_blur: Real, 0.0
[-🫴bevel]
 - z_depth: Real, 0.0
 - amount: Real, 0.75
 - blend_method: Integer, 13
 - type: Integer, 1
 - color1: Color, ffffffff
 - color2: Color, 000000ff
 - angle: Angle, 89.058815
 - depth: Real, 0.5819661441
 - softness: Real, 0.3276240462
 - use_luma: Bool, True
 - solid: Bool, True
 - fake_origin: Vector, {'x': '0.0000000000', 'y': '0.0000000000'}
[-🔵circle 'Bouncy ball']
 - z_depth: Real, 0.0
 - amount: Real, 1.0
 - blend_method: Integer, 0
 - color: Color, ff0000ff
 - radius: Real, 1.0
 - feather: Real, 0.0
 - origin: Vector, {'x': '0.0000000000', 'y': '0.0000000000'}
 - invert: Bool, True
[📂group 'Shadow']
 - z_depth: Real, 0.0
 - amount: Real, 1.0
 - blend_method: Integer, 1
 - origin: Vector, {'x': '0.0000000000', 'y': '-1.6666666269'}
 - transformation:
     - offset = Vector, {'x': '0.0000000000', 'y': '-1.6003249884'}
     - angle = Angle, 0.0
     - skew_angle = Angle, 0.0
     - scale = Vector, {'x': '1.0000000000', 'y': '0.3899480104'}
 - canvas: Canvas, [[--🔵circle 'Shadow circle'], [--🟠blur]]
 - color: Color, 00000072
 - radius: Real, 1.0
 - feather: Real, 0.0
 - invert: Bool, True
 - size: Vector, {'x': '0.2500000000', 'y': '0.2500000000'}
 - type: Integer, 1
 - time_dilation: Real, 1.0
 - time_offset: Time, 0f
 - children_lock: Bool, True
 - outline_grow: Real, 0.0
 - z_range: Bool, True
 - z_range_position: Real, 0.0
 - z_range_depth: Real, 0.0
 - z_range_blur: Real, 0.0
[-📂group 'Shadow']
 - z_depth: Real, 0.0
 - amount: Real, 1.0
 - blend_method: Integer, 1
 - origin: Vector, {'x': '0.0000000000', 'y': '-1.6666666269'}
 - transformation:
     - offset = Vector, {'x': '0.0000000000', 'y': '-1.6003249884'}
     - angle = Angle, 0.0
     - skew_angle = Angle, 0.0
     - scale = Vector, {'x': '1.0000000000', 'y': '0.3899480104'}
 - canvas: Canvas, [[--🔵circle 'Shadow circle'], [--🟠blur]]
 - color: Color, 00000072
 - radius: Real, 1.0
 - feather: Real, 0.0
 - invert: Bool, True
 - size: Vector, {'x': '0.2500000000', 'y': '0.2500000000'}
 - type: Integer, 1
 - time_dilation: Real, 1.0
 - time_offset: Time, 0f
 - children_lock: Bool, True
 - outline_grow: Real, 0.0
 - z_range: Bool, True
 - z_range_position: Real, 0.0
 - z_range_depth: Real, 0.0
 - z_range_blur: Real, 0.0
[📂group 'Background']
 - z_depth: Real, 0.0
 - amount: Real, 1.0
 - blend_method: Integer, 0
 - origin: Vector, {'x': '0.0000000000', 'y': '0.0000000000'}
 - transformation:
     - offset = Vector, {'x': '0.0000000000', 'y': '0.0000000000'}
     - angle = Angle, 0.0
     - skew_angle = Angle, 0.0
     - scale = Vector, {'x': '1.0000000000', 'y': '1.0000000000'}
 - canvas: Canvas, [[-▊solid_color 'wall'], [-🟦rectangle 'floor']]
 - color: Color, ffb355ff
 - point1: Vector, {'x': '-4.0130858421', 'y': '-2.3096354008'}
 - point2: Vector, {'x': '4.0234375000', 'y': '-0.9031249881'}
 - expand: Real, 0.0
 - invert: Bool, True
 - feather_x: Real, 0.0
 - feather_y: Real, 0.0
 - bevel: Real, 0.0
 - bevCircle: Bool, True
 - time_dilation: Real, 1.0
 - time_offset: Time, 0f
 - children_lock: Bool, True
 - outline_grow: Real, 0.0
 - z_range: Bool, True
 - z_range_position: Real, 0.0
 - z_range_depth: Real, 0.0
 - z_range_blur: Real, 0.0
[-🟦rectangle 'floor']
 - z_depth: Real, 0.0
 - amount: Real, 1.0
 - blend_method: Integer, 0
 - color: Color, ffb355ff
 - point1: Vector, {'x': '-4.0130858421', 'y': '-2.3096354008'}
 - point2: Vector, {'x': '4.0234375000', 'y': '-0.9031249881'}
 - expand: Real, 0.0
 - invert: Bool, True
 - feather_x: Real, 0.0
 - feather_y: Real, 0.0
 - bevel: Real, 0.0
 - bevCircle: Bool, True
[-▊solid_color 'wall']
 - z_depth: Real, 0.0
 - amount: Real, 1.0
 - blend_method: Integer, 0
 - color: Color, ffffffff
""".lstrip()
