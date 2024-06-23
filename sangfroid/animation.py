from sangfroid.keyframe import Keyframe
from sangfroid.layer import (
        Group, Field, TagAttrField, NamedChildField, TagField,
        )
from sangfroid.format import Format, Blank
from sangfroid.value.color import Color
from sangfroid.t import T
import bs4
import sangfroid.value as v

class MetadataTagField(Field):
    pass

class TagTimeAttrField(TagAttrField):
    def __init__(self,
                 default,
                 **kwargs,
                 ):
        super().__init__(
                type_ = T,
                default = default,
                type_override = str,
                **kwargs,
                )

    def __get__(self, obj, obj_type=None):
        s = super().__get__(obj, obj_type)

        if s is None:
            return None

        return T(s,
                 reference_tag = obj._tag,
                 )

class Animation(Group):
    """
    A Synfig animation.

    Synfig calls this a "canvas", but it also has a layer attribute
    called a "canvas". At first we called it "Sif", but that was
    no good, because it might be loaded from a `.sifz` or `.sfg` file.
    """

    version = TagAttrField(float,       1.2)
    width = TagAttrField(int,         480,
                         doc = "The width of the canvas, in pixels.",
                         )
    height = TagAttrField(int,         270,
                         doc = "The width of the canvas, in pixels.",
                          )
    xres = TagAttrField(float,       2834.645669,
                        doc = "The horizontal resolution.",
                        )
    yres = TagAttrField(float,       2834.645669,
                        doc = "The vertical resolution.",
                        )
    gamma_r = TagAttrField(float,       1.0)
    gamma_g = TagAttrField(float,       1.0)
    gamma_b = TagAttrField(float,       1.0)
    view_box = TagAttrField(str, '-4.0 2.25 4.0 -2.25') # XXX wrong
    antialias = TagAttrField(int,         1) # XXX enum?
    fps = TagAttrField(float,       24.0,
        doc = """
            The number of frames per second. Usually 24.

            (Can this be non-integer?)""",
           )
    begin_time = TagTimeAttrField(0,
           doc = """
            The time at which this animation starts.

            Almost always zero.""",
           )
    end_time = TagTimeAttrField('5s',
            doc = 'The time at which this animation ends.',
           )
    bgcolor = TagAttrField(str,         '0.5 0.5 0.5 1.0')

    background_first_color = MetadataTagField(v.Color, (0.88, 0.88, 0.88))
    background_rendering = MetadataTagField(v.Integer, 0)
    background_second_color = MetadataTagField(v.Color, (0.65, 0.65, 0.65))
    background_size = MetadataTagField(v.X_Y,     (15.0, 15.0))
    grid_color = MetadataTagField(v.Color, (0.623529, 0.623529, 0.623529))
    grid_show = MetadataTagField(v.Integer, 0)
    grid_size = MetadataTagField(v.X_Y, (0.25, 0.25))
    grid_snap = MetadataTagField(v.Integer, 0)
    guide_color = MetadataTagField(v.Color, (0.435294, 0.435294, 1.09))
    guide_show = MetadataTagField(v.Integer, 1)
    guide_snap = MetadataTagField(v.Integer, 0)
    jack_offset = MetadataTagField(v.Real, 0.0)
    onion_skin = MetadataTagField(v.Integer, 0)
    onion_skin_future = MetadataTagField(v.Integer, 0)
    onion_skin_keyframes = MetadataTagField(v.Integer, 1)
    onion_skin_past = MetadataTagField(v.Integer, 1)

    name = NamedChildField(str, doc = """
    The name of this animation.

    Not the filename, though it's often the same.
    """, default='Not yet named')

    desc = NamedChildField(str, doc = """
    A description of this animation.

    So you know what it is when you find it again next year.
    """, default='Animation')

    tag = TagField()

    def __init__(self, filename:str=None):
        """
        Args:
            filename: the name of the main file to load.
        """
        self._filename = filename

        if filename is None:
            self._format = Blank()
        else:
            self._format = Format.from_filename(filename)

        with self._format.main_file() as soup:
            self._soup = soup

        assert len(self._soup.contents)==1
        tag = self._soup.contents[0]
        super().__init__(
                tag = tag,
                )

    @property
    def name(self):
        return self._tag.find('name').string

    @property
    def size(self):
        """
        The height and width of the screen.

        Type:
            (int, int)
        """
        return (
                int(self._tag.attrs['width']),
                int(self._tag.attrs['height']),
                )

    @property
    def viewbox(self):
        """
        The coordinates of the edges of the screen.

        This is a tuple of four floats:
        `(left, bottom, right, top)`.

        Type:
            4-tuple of floats
        """
        return tuple([
            float(n) for n in
            self._tag.attrs['view-box'].split(' ')
            ])


    @property
    def begin_time(self):
        """
        The time at which this animation starts.

        Almost always zero.

        Type:
            T
        """
        return T(self._tag.attrs['begin-time'],
                 reference_tag = self._tag,
                 )

    def __len__(self):
        """
        The number of frames in this animation.

        Should be equal to `int(end_time)-int(begin_time)`.

        Note that this is one higher than the number of
        the last frame.

        Type:
            int
        """
        return int(T(-1, reference_tag=self._tag).frames)+1

    @property
    def background(self):
        """
        The background colour.

        Type:
            Color
        """
        triplet = tuple([
            float(n) for n in
            self._tag.attrs['bgcolor'].split(' ')
            ])
        result = Color(*triplet)
        return result

    @property
    def keyframes(self):
        """
        The defined keyframes.
        """
        return Keyframe.all_in_animation(self)
 
    def save(self, filename:str=None):
        """
        Saves the animation back out to disk.

        Args:
            filename: the filename to save the animation to.
                If None, we use the filename we loaded it from.
        """

        if filename is None:
            if self._format is None:
                raise ValueError(
                        "If you didn't give a filename at creation, "
                        "you must give one when you save."
                        )
            filename = self._format.filename
        else:
            new_format = Format.from_filename(filename,
                                              load = False,
                                              )
            if new_format!=self._format:
                # XXX copy the images over
                self._format = new_format

        self._format.save(
                content = self._soup,
                filename = filename,
                )

__all__ = [
        'Animation',
        ]
