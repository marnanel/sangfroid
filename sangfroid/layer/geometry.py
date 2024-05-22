from sangfroid.layer import Layer
import sangfroid.value as v

@Layer.handles_type()
class Star(Layer):
    SYMBOL = '⭐'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "origin": v.Vector,
        "invert": v.Bool,
        "antialias": v.Bool,
        "feather": v.Real,
        "blurtype": v.Integer,
        "winding_style": v.Integer,
        "radius1": v.Real,
        "radius2": v.Real,
        "angle": v.Angle,
        "points": v.Integer,
        "regular_polygon": v.Bool,
    }
    ### }}}

@Layer.handles_type()
class Solid_Color(Layer):
    SYMBOL = '▊'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
    }
    ### }}}

@Layer.handles_type()
class Region(Layer):
    SYMBOL = '🟤'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "origin": v.Vector,
        "invert": v.Bool,
        "antialias": v.Bool,
        "feather": v.Real,
        "blurtype": v.Integer,
        "winding_style": v.Integer,
        "bline": v.Bline,
    }
    ### }}}

@Layer.handles_type()
class Rectangle(Layer):
    SYMBOL = '🟦'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "point1": v.Vector,
        "point2": v.Vector,
        "expand": v.Real,
        "invert": v.Bool,
        "feather_x": v.Real,
        "feather_y": v.Real,
        "bevel": v.Real,
        "bevCircle": v.Bool,
    }
    ### }}}

@Layer.handles_type()
class Polygon(Layer):
    SYMBOL = '⭓'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "origin": v.Vector,
        "invert": v.Bool,
        "antialias": v.Bool,
        "feather": v.Real,
        "blurtype": v.Integer,
        "winding_style": v.Integer,
        "vector_list": v.Dynamic_List,
    }
    ### }}}

@Layer.handles_type()
class Outline(Layer):
    SYMBOL = '⭔'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "origin": v.Vector,
        "invert": v.Bool,
        "antialias": v.Bool,
        "feather": v.Real,
        "blurtype": v.Integer,
        "winding_style": v.Integer,
        "bline": v.Bline,
        "width": v.Real,
        "expand": v.Real,
        "sharp_cusps": v.Bool,
        "round_tip[0]": v.Bool,
        "round_tip[1]": v.Bool,
        "homogeneous_width": v.Bool,
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "origin": v.Vector,
        "invert": v.Bool,
        "antialias": v.Bool,
        "feather": v.Real,
        "blurtype": v.Integer,
        "winding_style": v.Integer,
        "bline": v.Bline,
        "width": v.Real,
        "expand": v.Real,
        "sharp_cusps": v.Bool,
        "round_tip[0]": v.Bool,
        "round_tip[1]": v.Bool,
        "homogeneous_width": v.Bool,
    }
    ### }}}

@Layer.handles_type()
class Circle(Layer):
    SYMBOL = '🔵'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "radius": v.Real,
        "feather": v.Real,
        "origin": v.Vector,
        "invert": v.Bool,
    }
    ### }}}

@Layer.handles_type()
class Checker_Board(Layer):
    SYMBOL = '🙾'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "origin": v.Vector,
        "size": v.Vector,
        "antialias": v.Bool,
    }
    ### }}}

@Layer.handles_type()
class Advanced_Outline(Layer):
    SYMBOL = '⬡'

    ### {{{
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "origin": v.Vector,
        "invert": v.Bool,
        "antialias": v.Bool,
        "feather": v.Real,
        "blurtype": v.Integer,
        "winding_style": v.Integer,
        "bline": v.Bline,
        "width": v.Real,
        "expand": v.Real,
        "start_tip": v.Integer,
        "end_tip": v.Integer,
        "cusp_type": v.Integer,
        "smoothness": v.Real,
        "homogeneous": v.Bool,
        "wplist": v.Wplist,
        "dash_enabled": v.Bool,
        "dilist": v.Dilist,
        "dash_offset": v.Real,
    }
    ### }}}
