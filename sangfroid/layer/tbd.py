from sangfroid.layer.layer import Layer
import sangfroid.value as v
import sangfroid.layer.field as f

"""
These are the layer types that we haven't got to yet.
"""

@Layer.handles_type()
class Xor_Pattern(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    origin               = f.ParamTagField(v.X_Y, (0.125, 0.125))
    size                 = f.ParamTagField(v.X_Y, (0.25, 0.25))

    ### }}}

@Layer.handles_type()
class Switch(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.0"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    transformation       = f.ParamTagField(v.Transformation, {
                                         'offset': (0.0, 0.0),
                                          'angle': 0.0,
                                     'skew_angle': 0.0,
                                          'scale': (1.0, 1.0),
                                        })
    canvas               = f.SwitchCanvasField()
    tl                   = f.ParamTagField(v.X_Y, (-0.5333333611, 0.5333333611))
    br                   = f.ParamTagField(v.X_Y, (0.5333333611, -0.5333333611))
    c                    = f.ParamTagField(v.Integer, 1)
    gamma_adjust         = f.ParamTagField(v.Real, 1.0)
    filename             = f.ParamTagField(v.String, 'drop.png')
    time_offset          = f.ParamTagField(v.Time, 0)
    time_dilation        = f.ParamTagField(v.Real, 1.0)
    children_lock        = f.ParamTagField(v.Bool, True)
    outline_grow         = f.ParamTagField(v.Real, 0.0)
    layer_name           = f.ParamTagField(v.String, 'drop.png')
    layer_depth          = f.ParamTagField(v.Integer, -1)

    ### }}}

@Layer.handles_type()
class Super_Sample(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.2"

    width                = f.ParamTagField(v.Integer, 2)
    height               = f.ParamTagField(v.Integer, 2)

    ### }}}

@Layer.handles_type()
class Sound(Layer):
    SYMBOL = '🔊'
    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    filename             = f.ParamTagField(v.String, 'laser.wav')
    delay                = f.ParamTagField(v.Time, 0)
    volume               = f.ParamTagField(v.Real, 1.0)

    ### }}}

@Layer.handles_type()
class Skeleton(Layer):
    SYMBOL = '💀'
    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 0.5)
    name                 = f.ParamTagField(v.String, 'skeleton')
    bones                = f.NotImplementedField("Static_List")

    ### }}}

@Layer.handles_type()
class Plant(Layer):
    SYMBOL = '🪴'
    ### {{{
    SYNFIG_VERSION = "0.2"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    bline                = f.NotImplementedField("Bline")
    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    gradient             = f.ParamTagField(v.Gradient, {0.0:(1.0, 1.0, 1.0, 1.0),1.0:(0.0, 0.0, 0.0, 1.0)})
    split_angle          = f.ParamTagField(v.Angle, 10.0)
    gravity              = f.ParamTagField(v.X_Y, (0.0, -0.1000000015))
    velocity             = f.ParamTagField(v.Real, 0.3)
    perp_velocity        = f.ParamTagField(v.Real, 0.0)
    size                 = f.ParamTagField(v.Real, 0.015)
    size_as_alpha        = f.ParamTagField(v.Bool, True)
    reverse              = f.ParamTagField(v.Bool, True)
    step                 = f.ParamTagField(v.Real, 0.01)
    seed                 = f.ParamTagField(v.Integer, 1700432811)
    splits               = f.ParamTagField(v.Integer, 5)
    sprouts              = f.ParamTagField(v.Integer, 10)
    random_factor        = f.ParamTagField(v.Real, 0.2)
    drag                 = f.ParamTagField(v.Real, 0.1)
    use_width            = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Filter_Group(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.STRAIGHT)
    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    transformation       = f.ParamTagField(v.Transformation, {
                                         'offset': (0.0, 0.0),
                                          'angle': 0.0,
                                     'skew_angle': 0.0,
                                          'scale': (1.0, 1.0),
                                        })
    canvas               = f.ParamTagField(v.Canvas, [])
    time_dilation        = f.ParamTagField(v.Real, 1.0)
    time_offset          = f.ParamTagField(v.Time, 0)
    children_lock        = f.ParamTagField(v.Bool, True)
    outline_grow         = f.ParamTagField(v.Real, 0.0)

    ### }}}

@Layer.handles_type()
class Duplicate(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    index                = f.DuplicatesIndexField(None)

    ### }}}

@Layer.handles_type()
class Spiral_Gradient(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.2"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    gradient             = f.ParamTagField(v.Gradient, {0.0:(1.0, 1.0, 1.0, 1.0),1.0:(0.0, 0.0, 0.0, 1.0)})
    center               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    radius               = f.ParamTagField(v.Real, 0.5)
    angle                = f.ParamTagField(v.Angle, 0.0)
    clockwise            = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Radial_Gradient(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.2"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    gradient             = f.ParamTagField(v.Gradient, {0.0:(1.0, 1.0, 1.0, 1.0),1.0:(0.0, 0.0, 0.0, 1.0)})
    center               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    radius               = f.ParamTagField(v.Real, 0.5)
    loop                 = f.ParamTagField(v.Bool, True)
    zigzag               = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Noise(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.0"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    gradient             = f.ParamTagField(v.Gradient, {0.0:(1.0, 1.0, 1.0, 1.0),1.0:(0.0, 0.0, 0.0, 1.0)})
    seed                 = f.ParamTagField(v.Integer, 1700432620)
    size                 = f.ParamTagField(v.X_Y, (1.0, 1.0))
    smooth               = f.ParamTagField(v.Integer, 2)
    detail               = f.ParamTagField(v.Integer, 4)
    speed                = f.ParamTagField(v.Real, 0.0)
    turbulent            = f.ParamTagField(v.Bool, True)
    do_alpha             = f.ParamTagField(v.Bool, True)
    super_sample         = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Linear_Gradient(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    p1                   = f.ParamTagField(v.X_Y, (1.0, 1.0))
    p2                   = f.ParamTagField(v.X_Y, (-1.0, -1.0))
    gradient             = f.ParamTagField(v.Gradient, {0.0:(1.0, 1.0, 1.0, 1.0),1.0:(0.0, 0.0, 0.0, 1.0)})
    loop                 = f.ParamTagField(v.Bool, True)
    zigzag               = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Curve_Gradient(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.0"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    width                = f.ParamTagField(v.Real, 0.0166666667)
    bline                = f.NotImplementedField("Bline")
    gradient             = f.ParamTagField(v.Gradient, {0.0:(1.0, 1.0, 1.0, 1.0),1.0:(0.0, 0.0, 0.0, 1.0)})
    loop                 = f.ParamTagField(v.Bool, True)
    zigzag               = f.ParamTagField(v.Bool, True)
    perpendicular        = f.ParamTagField(v.Bool, True)
    fast                 = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Conical_Gradient(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.2"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    gradient             = f.ParamTagField(v.Gradient, {0.0:(1.0, 1.0, 1.0, 1.0),1.0:(0.0, 0.0, 0.0, 1.0)})
    center               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    angle                = f.ParamTagField(v.Angle, 0.0)
    symmetric            = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Mandelbrot(Layer):
    SYMBOL = '🎨'
    ### {{{
    SYNFIG_VERSION = "0.2"

    iterations           = f.ParamTagField(v.Integer, 32)
    bailout              = f.ParamTagField(v.Real, 2.0)
    broken               = f.ParamTagField(v.Bool, True)
    distort_inside       = f.ParamTagField(v.Bool, True)
    shade_inside         = f.ParamTagField(v.Bool, True)
    solid_inside         = f.ParamTagField(v.Bool, True)
    invert_inside        = f.ParamTagField(v.Bool, True)
    gradient_inside      = f.ParamTagField(v.Gradient, {0.0:(1.0, 0.0, 0.0, 1.0),1.0:(1.0, 1.0, 0.0, 1.0)})
    gradient_offset_inside = f.ParamTagField(v.Real, 0.0)
    gradient_loop_inside = f.ParamTagField(v.Bool, True)
    distort_outside      = f.ParamTagField(v.Bool, True)
    shade_outside        = f.ParamTagField(v.Bool, True)
    solid_outside        = f.ParamTagField(v.Bool, True)
    invert_outside       = f.ParamTagField(v.Bool, True)
    gradient_outside     = f.ParamTagField(v.Gradient, {0.0:(0.0, 0.0, 0.0, 0.0),1.0:(0.0, 0.0, 0.0, 1.0)})
    smooth_outside       = f.ParamTagField(v.Bool, True)
    gradient_offset_outside = f.ParamTagField(v.Real, 0.0)
    gradient_scale_outside = f.ParamTagField(v.Real, 1.0)

    ### }}}

@Layer.handles_type()
class Julia(Layer):
    SYMBOL = '🎨'
    ### {{{
    SYNFIG_VERSION = "0.1"

    icolor               = f.ParamTagField(v.Color, (0.0, 0.0, 0.0, 1.0))
    ocolor               = f.ParamTagField(v.Color, (0.0, 0.0, 0.0, 1.0))
    color_shift          = f.ParamTagField(v.Angle, 0.0)
    iterations           = f.ParamTagField(v.Integer, 32)
    seed                 = f.ParamTagField(v.X_Y, (0.0, 0.0))
    bailout              = f.ParamTagField(v.Real, 2.0)
    distort_inside       = f.ParamTagField(v.Bool, True)
    shade_inside         = f.ParamTagField(v.Bool, True)
    solid_inside         = f.ParamTagField(v.Bool, True)
    invert_inside        = f.ParamTagField(v.Bool, True)
    color_inside         = f.ParamTagField(v.Bool, True)
    distort_outside      = f.ParamTagField(v.Bool, True)
    shade_outside        = f.ParamTagField(v.Bool, True)
    solid_outside        = f.ParamTagField(v.Bool, True)
    invert_outside       = f.ParamTagField(v.Bool, True)
    color_outside        = f.ParamTagField(v.Bool, True)
    color_cycle          = f.ParamTagField(v.Bool, True)
    smooth_outside       = f.ParamTagField(v.Bool, True)
    broken               = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Lumakey(Layer):
    SYMBOL = '🗝️'
    ### {{{
    SYNFIG_VERSION = "0.2"

    z_depth              = f.ParamTagField(v.Real, 0.0)

    ### }}}

@Layer.handles_type()
class Halftone3(Layer):
    SYMBOL = '▓'
    ### {{{
    SYNFIG_VERSION = "0.0"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.STRAIGHT)
    size                 = f.ParamTagField(v.X_Y, (0.25, 0.25))
    type_                = f.ParamTagField(v.Integer, 0)
    subtractive          = f.ParamTagField(v.Bool, True)
    color                = f.ParamArrayField(v.Color, (0.0, 1.0, 1.0, 1.0))
    tone                 = f.ParamArrayField(v.Tone, default=None)

    ### }}}

@Layer.handles_type()
class Halftone2(Layer):
    SYMBOL = '▒'
    ### {{{
    SYNFIG_VERSION = "0.0"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.STRAIGHT)
    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    angle                = f.ParamTagField(v.Angle, 0.0)
    size                 = f.ParamTagField(v.X_Y, (0.25, 0.25))
    color_light          = f.ParamTagField(v.Color, (1.0, 1.0, 1.0, 1.0))
    color_dark           = f.ParamTagField(v.Color, (0.0, 0.0, 0.0, 1.0))
    type_                = f.ParamTagField(v.Integer, 0)

    ### }}}

@Layer.handles_type()
class Colorcorrect(Layer):
    SYMBOL = '👍'
    ### {{{
    SYNFIG_VERSION = "0.1"

    hue_adjust           = f.ParamTagField(v.Angle, 0.0)
    brightness           = f.ParamTagField(v.Real, 0.0)
    contrast             = f.ParamTagField(v.Real, 1.0)
    exposure             = f.ParamTagField(v.Real, 0.0)
    gamma                = f.ParamTagField(v.Real, 1.0)

    ### }}}

@Layer.handles_type()
class Clamp(Layer):
    SYMBOL = '🗜️'
    ### {{{
    SYNFIG_VERSION = "0.2"

    invert_negative      = f.ParamTagField(v.Bool, True)
    clamp_ceiling        = f.ParamTagField(v.Bool, True)
    ceiling              = f.ParamTagField(v.Real, 1.0)
    floor                = f.ParamTagField(v.Real, 0.0)

    ### }}}

@Layer.handles_type()
class Chromakey(Layer):
    SYMBOL = '🔑'
    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    key_color            = f.ParamTagField(v.Color, (0.0, 1.0, 0.0, 1.0))
    lower_bound          = f.ParamTagField(v.Real, 0.001)
    upper_bound          = f.ParamTagField(v.Real, 0.001)
    supersample_width    = f.ParamTagField(v.Integer, 2)
    supersample_height   = f.ParamTagField(v.Integer, 2)
    desaturate           = f.ParamTagField(v.Bool, True)
    invert               = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Simple_Circle(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    color                = f.ParamTagField(v.Color, (1.0, 1.0, 1.0, 1.0))
    center               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    radius               = f.ParamTagField(v.Real, 0.5)

    ### }}}

@Layer.handles_type()
class Metaballs(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.1"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.COMPOSITE)
    gradient             = f.ParamTagField(v.Gradient, {0.0:(1.0, 1.0, 1.0, 1.0),1.0:(0.0, 0.0, 0.0, 1.0)})
    centers              = f.NotImplementedField("Dynamic_List")
    radii                = f.NotImplementedField("Dynamic_List")
    weights              = f.NotImplementedField("Dynamic_List")
    threshold            = f.ParamTagField(v.Real, 0.0)
    threshold2           = f.ParamTagField(v.Real, 1.0)
    positive             = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Warp(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.2"

    src_tl               = f.ParamTagField(v.X_Y, (-2.0, 2.0))
    src_br               = f.ParamTagField(v.X_Y, (2.0, -2.0))
    dest_tl              = f.ParamTagField(v.X_Y, (-1.7999999523, 2.0999999046))
    dest_tr              = f.ParamTagField(v.X_Y, (1.7999999523, 2.0999999046))
    dest_br              = f.ParamTagField(v.X_Y, (2.2000000477, -2.0))
    dest_bl              = f.ParamTagField(v.X_Y, (-2.2000000477, -2.0))
    clip                 = f.ParamTagField(v.Bool, True)
    interpolation        = f.ParamTagField(v.Integer, 3)

    ### }}}

@Layer.handles_type()
class Twirl(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.1"

    center               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    radius               = f.ParamTagField(v.Real, 1.0)
    rotations            = f.ParamTagField(v.Angle, 0.0)
    distort_inside       = f.ParamTagField(v.Bool, True)
    distort_outside      = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Stretch(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.1"

    amount               = f.ParamTagField(v.X_Y, (1.0, 1.0))
    center               = f.ParamTagField(v.X_Y, (0.0, 0.0))

    ### }}}

@Layer.handles_type()
class Spherize(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.2"

    center               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    radius               = f.ParamTagField(v.Real, 1.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    clip                 = f.ParamTagField(v.Bool, True)
    type_                = f.ParamTagField(v.Integer, 0)

    ### }}}

@Layer.handles_type()
class Skeleton_Deformation(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.2"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.STRAIGHT)
    bones                = f.NotImplementedField("Static_List")
    point1               = f.ParamTagField(v.X_Y, (-4.0, 4.0))
    point2               = f.ParamTagField(v.X_Y, (4.0, -4.0))
    x_subdivisions       = f.ParamTagField(v.Integer, 32)
    y_subdivisions       = f.ParamTagField(v.Integer, 32)

    ### }}}

@Layer.handles_type()
class Noise_Distort(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.0"

    z_depth              = f.ParamTagField(v.Real, 0.0)
    amount               = f.ParamTagField(v.Real, 1.0)
    blend_method         = f.ParamTagField(v.BlendMethod, v.BlendMethod.STRAIGHT)
    displacement         = f.ParamTagField(v.X_Y, (0.25, 0.25))
    size                 = f.ParamTagField(v.X_Y, (1.0, 1.0))
    seed                 = f.ParamTagField(v.Integer, 1700432512)
    smooth               = f.ParamTagField(v.Integer, 2)
    detail               = f.ParamTagField(v.Integer, 4)
    speed                = f.ParamTagField(v.Real, 0.0)
    turbulent            = f.ParamTagField(v.Bool, True)

    ### }}}

@Layer.handles_type()
class Inside_Out(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.1"

    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0))

    ### }}}

@Layer.handles_type()
class Curve_Warp(Layer):
    SYMBOL = 'X'
    ### {{{
    SYNFIG_VERSION = "0.0"

    origin               = f.ParamTagField(v.X_Y, (0.0, 0.0))
    perp_width           = f.ParamTagField(v.Real, 1.0)
    start_point          = f.ParamTagField(v.X_Y, (-2.5, -0.5))
    end_point            = f.ParamTagField(v.X_Y, (2.5, -0.3000000119))
    bline                = f.NotImplementedField("Bline")
    fast                 = f.ParamTagField(v.Bool, True)

    ### }}}


