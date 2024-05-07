import copy
import bs4
import sangfroid.value as v
from sangfroid.registry import Registry
from sangfroid.layer.field import Field
from sangfroid.util import (
        normalise_synfig_layer_type_name,
        type_and_str_to_value,
        type_and_value_to_str,
        )

class Layer:

    SYMBOL = '?' # fallback

    FIELDS = Field.dict_of(
            Field('type',             str,         None),
            Field('active',           bool,        True),
            Field('exclude_from_rendering', bool,  False),
            Field('version',          float,       None),
            Field('desc',             str,         None),
            Field('z_depth',          v.Real,      0.0),
            Field('amount',           v.Real,      1.0),
            Field('blend_method',     v.Integer,     0), # XXX ??
            Field('origin',           v.XY,        (0.0, 0.0)),
            Field('transformation',   v.Transformation,
                                      {
                                          Field('offset', v.XY, (0.0, 0.0)),
                                          Field('angle', v.Angle, 0.0),
                                          Field('skew_angle', v.Angle, 0.0),
                                          Field('scale', v.XY, (0.0, 0.0)),
                                          }),
            Field('canvas',           v.Canvas,    None),
            Field('time_dilation',    v.Real,      1.0),
            Field('time_offset',      v.Time,      0),
            Field('children_lock',    v.Bool,      True),
            Field('outline_grow',     v.Real,      0.0),
            Field('z_range',          v.Bool,      False),
            Field('z_range_position', v.Real,      0.0),
            Field('z_range_depth',    v.Real,      0.0),
            Field('z_range_blur',     v.Real,      0.0),
            )

     ########################

    def __init__(self, tag):
        self.tag = tag

    def __getattr__(self, f):
        if f not in self.FIELDS:
            raise KeyError(f)

        print("9800 GET", f)
        field = self.FIELDS[f]
        if field.in_params:
            result = self._get_param(field.name)
        else:
            result = type_and_value_to_str(
                    field.type_,
                    self.tag.get(field.name, None),
                    )
        print("9850", field, result)
        print("9851", str(self.tag)[:80])

        return result

    def __setattr__(self, f, v):
        if f not in self.FIELDS:
            raise KeyError(f)

        print("9900 SET", f)
        field = self.FIELDS[f]

        raise ValueError(field)

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

    def __setitem__(self, f, val):
        found = self.tag.find('param', attrs={'name': f})
        if found is None:
            raise KeyError(f)
        old_value = _name_and_value_of(found)[1]

        if isinstance(val, v.Value):
            if not isinstance(val, old_value.__class__):
                raise TypeError(val.__class__)

            new_value = val
        else:
            new_value = old_value.__class__(val)

        old_value.tag.replace_with(new_value.tag)

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

    def find_all(self,
                 *args,
                 recursive=True,
                 **kwargs,
                 ):

        matching_special = None

        if len(args)>1:
            raise v.ValueError(
                    "You can only give one positional argument.")
        elif len(args)==1:

            if (
                    isinstance(args[0], str) or
                    (isinstance(args[0], type) and
                     issubclass(args[0], Layer))
                    ):
                if 'type' in kwargs:
                    raise v.ValueError(
                            "You can't give a type in both the positional "
                            "and keyword arguments.")

                kwargs['type'] = args[0]

            elif isinstance(args[0], bool):
                matching_special = args[0]

            elif hasattr(args[0], '__call__'):
                matching_special = args[0]

            else:
                raise TypeError(args[0])

        if 'attrs' in kwargs:
            for k,v in kwargs['attrs'].items():
                if k in kwargs:
                    raise v.ValueError("{k} specified both as a kwarg and in attrs")
                kwargs[k] = v

            del kwargs['attrs']

        """
        for k,v in kwargs.items():
            if k=='type':
                if isinstance(v, type) and issubclass(v, Layer):
                    v = v.__name__

                v = normalise_synfig_layer_type_name(v)
                match_in_attribs[k] = v

            else blah
            """
        for k,v in kwargs.items():
            if k=='type':
                if not isinstance(v, str):
                    v = v.__name__

                kwargs[k] = v.lower().replace('_', '')

        def matcher(found_tag):
            if found_tag.name!='layer':
                return False

            found_layer = Layer.from_tag(found_tag)

            if matching_special is None:

                for k, want_value in kwargs.items():
                    where_to_look = found_layer.FIELDS.get(k, None)

                    if k in (
                            'type',
                            ):
                        want_value = want_value.lower()

                    if where_to_look.in_params:
                        found_tag_value = found_layer._get_param(k)
                    else:
                        found_tag_value = found_tag.get(k, None)

                    if found_tag_value==want_value:
                        return True


                    """
                        if found_tag_attr==v:
                            return True

                if match_in_params:
                    for param in found_tag.find_all('param',
                                              recursive=False):
                        if param['name'] in match_in_params:
                            t = [n for n in param.children
                                 if isinstance(n, bs4.element.Tag)][0]

                            value = v.Value.from_tag(t)

                            if match_in_params[param['name']] == value:
                                return True
                                """

                return False

            elif isinstance(matching_special, bool):
                return matching_special

            else:
                return matching_special(found_tag)

            raise v.ValueError(found_tag)

        result = [
                self.from_tag(x) for x in
                self.tag.find_all(matcher,
                                  recursive=recursive,
                                  )
                ]

        return result

    @property
    def children(self):
        return
        yield

    def find(self, *args, **kwargs):
        items = self.find_all(*args, **kwargs)
        if items:
            return items[0]
        else:
            return None

    __call__ = find

    ########################

    handles_type = Registry()

    @classmethod
    def from_tag(cls, tag):
        tag_type = tag.get('type', None)
        if tag_type is None:
            raise v.ValueError(
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

    def _get_param(self, k):
        tag = self.tag.find('param',
                            attribs={
                                'name': k,
                                })
        if tag is None:
            return None

        raise ValueError(f"{k}, {tag}")

    @classmethod
    def _prep_param(cls, f, v):
        result = bs4.Tag('param')
        result['name'] = f
        result.append(v.tag)
        return result
  
#####################
# Specific layer types.
# I'm moving these out to their own modules.
# These are the ones I haven't got to yet.
######################

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
        raise v.ValueError(f"param is not a <param>: {tag}")

    name = tag.get('name', None)
    if name is None:
        raise v.ValueError(f"param has no 'name' field: {tag}")

    value_tags = [tag for tag in tag.children
                  if isinstance(tag, bs4.element.Tag)
                  ]

    if len(value_tags)!=1:
        raise v.ValueError(f"param should have one value: {tag}")

    value_tag = value_tags[0]

    value = v.Value.from_tag(value_tag)
    return name, value
