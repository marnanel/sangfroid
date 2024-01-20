import bs4
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

    def __getitem__(self, f):
        found = self.tag.find('param', attrs={'name': f})
        if found is None:
            raise KeyError(f)
        return _name_and_value_of(found)[1]

    def __contains__(self, f):
        found = self.tag.find(
                'param',
                attrs={'name': f},
                )
        return found is not None

    @property
    def depth(self):
        cursor = self.tag.parent
        result = 0
        while cursor is not None:
            if cursor.name=='layer':
                result += 1
            cursor = cursor.parent
        return result

    def _find_or_find_all(self,
                          *args, **kwargs):
        if len(args)>1:
            raise ValueError(
                    "You can only give one positional argument.")
        elif len(args)==1:
            if 'type' in kwargs:
                raise ValueError(
                        "You can't give a type in both the positional "
                        "and keyword arguments.")
            kwargs['type'] = args[0]

        for k,v in kwargs.items():
            if isinstance(v, str):
                v = v.lower()
                def _case_insensitive_match(s):
                    if s is None:
                        return False
                    return s.lower()==v
                kwargs[k] = _case_insensitive_match

        find_all = kwargs.get('find_all', False)
        if 'find_all' in kwargs:
            del kwargs['find_all']

        if find_all:
            result = [
                    Layer(tag=t)
                    for t in self.tag.find_all('layer', attrs=kwargs)
                    ]

        else:
            layer = self.tag.find('layer', attrs=kwargs)
            if layer is None:
                result = None
            else:
                result = Layer(layer)

        return result

    def find(self, *args, **kwargs):
        return self._find_or_find_all(*args, find_all = False, **kwargs)

    def find_all(self, *args, **kwargs):
        return self._find_or_find_all(*args, find_all = True, **kwargs)

    __call__ = find

    ########################

    handles_type = Registry()

    @classmethod
    def from_tag(cls, tag):
        tag_type = tag.get('type', None)
        if tag_type is None:
            raise ValueError(
                    f"tag has no 'type' field: {tag}")
        return cls.handles_type.from_name(name=tag_type)(tag)

    def _as_dict(self):
        return dict([
            _name_and_value_of(param)
            for param in self.tag.find_all('param')
            ])

    def items(self):
        return self._as_dict().items()

    def keys(self):
        return self._as_dict().keys()

    def values(self):
        return self._as_dict().values()

    def __iter__(self):
        return self._as_dict().__iter__()

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
    SYMBOL = '🎨'
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
    SYMBOL = '🎨'
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
    SYMBOL = '🗝️'
    PARAMS = {
        "z_depth": v.Real,
    }

@Layer.handles_type()
class Halftone3(Layer):
    SYMBOL = '▓'
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
    SYMBOL = '▒'
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
    SYMBOL = '👍'
    PARAMS = {
        "hue_adjust": v.Angle,
        "brightness": v.Real,
        "contrast": v.Real,
        "exposure": v.Real,
        "gamma": v.Real,
    }

@Layer.handles_type()
class Clamp(Layer):
    SYMBOL = '🗜️'
    PARAMS = {
        "invert_negative": v.Bool,
        "clamp_ceiling": v.Bool,
        "ceiling": v.Real,
        "floor": v.Real,
    }

@Layer.handles_type()
class Chromakey(Layer):
    SYMBOL = '🔑'
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

def _name_and_value_of(tag):
    if tag.name!='param':
        raise ValueError(f"param is not a <param>: {tag}")

    name = tag.get('name', None)
    if name is None:
        raise ValueError(f"param has no 'name' field: {tag}")

    value_tags = [tag for tag in tag.children
                  if isinstance(tag, bs4.element.Tag)
                  ]

    if len(value_tags)!=1:
        raise ValueError(f"param should have one value: {tag}")

    value_tag = value_tags[0]

    value = Value.from_tag(value_tag)
    return name, value
