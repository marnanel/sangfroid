from sangfroid.value import Value
from sangfroid.registry import Registry

class Layer:

    SYMBOL = '?' # fallback

    ########################

    def __init__(self, tag):
        self.tag = tag

        # 'group' field?
        self.active = tag.get('active', True)
        self.synfig_version = tag.get('version', None)
        self.exclude_from_rendering = tag.get(
                'exclude_from_rendering', False)

        def name_and_value_of(tag):
            name = tag.get('name', None)

            if name is None:
                raise ValueError(f"param has no name: {tag}")

            use = tag.get("use", None)

            first_tag_child = None
            for c in tag.children:
                if hasattr(c, 'contents'):
                    first_tag_child = c
                    break

            if first_tag_child is None:
                if use is None:
                    raise ValueError(f"param has no value: {tag}")
                else:
                    print("(warning: 'use' is not yet implemented)")
                    value = 0

            else:
                if use is not None:
                    raise ValueError("param has both use and value: {tag}")
                value = Value.from_tag(tag=first_tag_child)

            return name, value

        self.params = dict([
            name_and_value_of(param)
            for param in tag.find_all('param')
            ])

    @property
    def desc(self):
        result = self.tag.get('desc', None)
        if result is not None:
            return result

        node = self.tag.find('desc')
        if node is not None:
            return node.string

        return None

    @property
    def parent(self):
        cursor = self.tag.parent
        while cursor is not None:
            print("???", cursor.name)
            if cursor.name=='layer':
                return Layer.from_tag(cursor)
                return cursor
            cursor = cursor.parent

    def __repr__(self):
        result = '['
        result += ('-'*self.depth)
        result += self.SYMBOL
        result += self.__class__.__name__.lower()
        desc = self.desc
        if desc is not None:
            result += ' '
            result += repr(desc)
        result += ']'
        return result

    @property
    def depth(self):
        cursor = self.tag.parent
        result = 0
        while cursor is not None:
            if cursor.name=='layer':
                result += 1
            cursor = cursor.parent
        return result

    ########################

    handles_type = Registry()

    @classmethod
    def from_tag(cls, tag):
        tag_type = tag.get('type', None)
        if tag_type is None:
            raise ValueError(
                    "layer has no 'type' field.")

        if tag_type not in cls.handles_type.handlers:
            raise ValueError(
                    f"This layer is a {tag_type}, which I don't know how "
                    "to handle."
                    )
        result = cls.handles_type.handlers[tag_type]._from_tag_inner(tag)

        return result

    @classmethod
    def _from_tag_inner(cls, tag):
        if cls==Layer:
            raise NotImplementedError()

        return cls(tag)

#####################
# Specific layer types.
# I'm moving these out to their own modules.
# These are the ones I haven't got to yet.
######################
import sangfroid.value as v

@Layer.handles_type()
class Xor_Pattern(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "origin": v.Vector,
        "size": v.Vector,
    }

@Layer.handles_type()
class Text(Layer):
    SYMBOL = '𝕋'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "text": v.String,
        "color": v.Color,
        "family": v.String,
        "style": v.Integer,
        "weight": v.Integer,
        "direction": v.Integer,
        "compress": v.Real,
        "vcompress": v.Real,
        "size": v.Vector,
        "orient": v.Vector,
        "origin": v.Vector,
        "use_kerning": v.Bool,
        "grid_fit": v.Bool,
        "invert": v.Bool,
    }

@Layer.handles_type()
class Switch(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "origin": v.Vector,
        "transformation": v.Composite,
        "canvas": v.Canvas,
        "time_dilation": v.Real,
        "time_offset": v.Time,
        "children_lock": v.Bool,
        "outline_grow": v.Real,
        "layer_name": v.String,
        "layer_depth": v.Integer,
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "origin": v.Vector,
        "transformation": v.Composite,
        "canvas": v.Canvas,
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "tl": v.Vector,
        "br": v.Vector,
        "c": v.Integer,
        "gamma_adjust": v.Real,
        "filename": v.String,
        "time_offset": v.Time,
        "time_dilation": v.Real,
        "time_offset": v.Time,
        "children_lock": v.Bool,
        "outline_grow": v.Real,
        "layer_name": v.String,
        "layer_depth": v.Integer,
    }

@Layer.handles_type()
class Super_Sample(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "width": v.Integer,
        "height": v.Integer,
    }

@Layer.handles_type()
class Sound(Layer):
    SYMBOL = '🔊'
    PARAMS = {
        "z_depth": v.Real,
        "filename": v.String,
        "delay": v.Time,
        "volume": v.Real,
    }

@Layer.handles_type()
class Skeleton(Layer):
    SYMBOL = '💀'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "name": v.String,
        "bones": v.Static_List,
    }

@Layer.handles_type()
class Plant(Layer):
    SYMBOL = '🪴'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "bline": v.Bline,
        "origin": v.Vector,
        "gradient": v.Gradient,
        "split_angle": v.Angle,
        "gravity": v.Vector,
        "velocity": v.Real,
        "perp_velocity": v.Real,
        "size": v.Real,
        "size_as_alpha": v.Bool,
        "reverse": v.Bool,
        "step": v.Real,
        "seed": v.Integer,
        "splits": v.Integer,
        "sprouts": v.Integer,
        "random_factor": v.Real,
        "drag": v.Real,
        "use_width": v.Bool,
    }

@Layer.handles_type()
class Filter_Group(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "origin": v.Vector,
        "transformation": v.Composite,
        "canvas": v.Canvas,
        "time_dilation": v.Real,
        "time_offset": v.Time,
        "children_lock": v.Bool,
        "outline_grow": v.Real,
    }

@Layer.handles_type()
class Duplicate(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
    }

@Layer.handles_type()
class Spiral_Gradient(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "gradient": v.Gradient,
        "center": v.Vector,
        "radius": v.Real,
        "angle": v.Angle,
        "clockwise": v.Bool,
    }

@Layer.handles_type()
class Radial_Gradient(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "gradient": v.Gradient,
        "center": v.Vector,
        "radius": v.Real,
        "loop": v.Bool,
        "zigzag": v.Bool,
    }

@Layer.handles_type()
class Noise(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "gradient": v.Gradient,
        "seed": v.Integer,
        "size": v.Vector,
        "smooth": v.Integer,
        "detail": v.Integer,
        "speed": v.Real,
        "turbulent": v.Bool,
        "do_alpha": v.Bool,
        "super_sample": v.Bool,
    }

@Layer.handles_type()
class Linear_Gradient(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "p1": v.Vector,
        "p2": v.Vector,
        "gradient": v.Gradient,
        "loop": v.Bool,
        "zigzag": v.Bool,
    }

@Layer.handles_type()
class Curve_Gradient(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "origin": v.Vector,
        "width": v.Real,
        "bline": v.Bline,
        "gradient": v.Gradient,
        "loop": v.Bool,
        "zigzag": v.Bool,
        "perpendicular": v.Bool,
        "fast": v.Bool,
    }

@Layer.handles_type()
class Conical_Gradient(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "gradient": v.Gradient,
        "center": v.Vector,
        "angle": v.Angle,
        "symmetric": v.Bool,
    }

@Layer.handles_type()
class Mandelbrot(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "iterations": v.Integer,
        "bailout": v.Real,
        "broken": v.Bool,
        "distort_inside": v.Bool,
        "shade_inside": v.Bool,
        "solid_inside": v.Bool,
        "invert_inside": v.Bool,
        "gradient_inside": v.Gradient,
        "gradient_offset_inside": v.Real,
        "gradient_loop_inside": v.Bool,
        "distort_outside": v.Bool,
        "shade_outside": v.Bool,
        "solid_outside": v.Bool,
        "invert_outside": v.Bool,
        "gradient_outside": v.Gradient,
        "smooth_outside": v.Bool,
        "gradient_offset_outside": v.Real,
        "gradient_scale_outside": v.Real,
    }

@Layer.handles_type()
class Julia(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "icolor": v.Color,
        "ocolor": v.Color,
        "color_shift": v.Angle,
        "iterations": v.Integer,
        "seed": v.Vector,
        "bailout": v.Real,
        "distort_inside": v.Bool,
        "shade_inside": v.Bool,
        "solid_inside": v.Bool,
        "invert_inside": v.Bool,
        "color_inside": v.Bool,
        "distort_outside": v.Bool,
        "shade_outside": v.Bool,
        "solid_outside": v.Bool,
        "invert_outside": v.Bool,
        "color_outside": v.Bool,
        "color_cycle": v.Bool,
        "smooth_outside": v.Bool,
        "broken": v.Bool,
    }

@Layer.handles_type()
class Lumakey(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
    }

@Layer.handles_type()
class Halftone3(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "size": v.Vector,
        "type": v.Integer,
        "subtractive": v.Bool,
        "color[0]": v.Color,
        "tone[0].origin": v.Vector,
        "tone[0].angle": v.Angle,
        "color[1]": v.Color,
        "tone[1].origin": v.Vector,
        "tone[1].angle": v.Angle,
        "color[2]": v.Color,
        "tone[2].origin": v.Vector,
        "tone[2].angle": v.Angle,
    }

@Layer.handles_type()
class Halftone2(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "origin": v.Vector,
        "angle": v.Angle,
        "size": v.Vector,
        "color_light": v.Color,
        "color_dark": v.Color,
        "type": v.Integer,
    }

@Layer.handles_type()
class Colorcorrect(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "hue_adjust": v.Angle,
        "brightness": v.Real,
        "contrast": v.Real,
        "exposure": v.Real,
        "gamma": v.Real,
    }

@Layer.handles_type()
class Clamp(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "invert_negative": v.Bool,
        "clamp_ceiling": v.Bool,
        "ceiling": v.Real,
        "floor": v.Real,
    }

@Layer.handles_type()
class Chromakey(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "key_color": v.Color,
        "lower_bound": v.Real,
        "upper_bound": v.Real,
        "supersample_width": v.Integer,
        "supersample_height": v.Integer,
        "desaturate": v.Bool,
        "invert": v.Bool,
    }

@Layer.handles_type()
class Simple_Circle(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "color": v.Color,
        "center": v.Vector,
        "radius": v.Real,
    }

@Layer.handles_type()
class Metaballs(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "gradient": v.Gradient,
        "centers": v.Dynamic_List,
        "radii": v.Dynamic_List,
        "weights": v.Dynamic_List,
        "threshold": v.Real,
        "threshold2": v.Real,
        "positive": v.Bool,
    }

@Layer.handles_type()
class Warp(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "src_tl": v.Vector,
        "src_br": v.Vector,
        "dest_tl": v.Vector,
        "dest_tr": v.Vector,
        "dest_br": v.Vector,
        "dest_bl": v.Vector,
        "clip": v.Bool,
        "interpolation": v.Integer,
    }

@Layer.handles_type()
class Twirl(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "center": v.Vector,
        "radius": v.Real,
        "rotations": v.Angle,
        "distort_inside": v.Bool,
        "distort_outside": v.Bool,
    }

@Layer.handles_type()
class Stretch(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "amount": v.Vector,
        "center": v.Vector,
    }

@Layer.handles_type()
class Spherize(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "center": v.Vector,
        "radius": v.Real,
        "amount": v.Real,
        "clip": v.Bool,
        "type": v.Integer,
    }

@Layer.handles_type()
class Skeleton_Deformation(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "bones": v.Static_List,
        "point1": v.Vector,
        "point2": v.Vector,
        "x_subdivisions": v.Integer,
        "y_subdivisions": v.Integer,
    }

@Layer.handles_type()
class Noise_Distort(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "z_depth": v.Real,
        "amount": v.Real,
        "blend_method": v.Integer,
        "displacement": v.Vector,
        "size": v.Vector,
        "seed": v.Integer,
        "smooth": v.Integer,
        "detail": v.Integer,
        "speed": v.Real,
        "turbulent": v.Bool,
    }

@Layer.handles_type()
class Inside_Out(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "origin": v.Vector,
    }

@Layer.handles_type()
class Curve_Warp(Layer):
    SYMBOL = 'X'
    PARAMS = {
        "origin": v.Vector,
        "perp_width": v.Real,
        "start_point": v.Vector,
        "end_point": v.Vector,
        "bline": v.Bline,
        "fast": v.Bool,
    }


