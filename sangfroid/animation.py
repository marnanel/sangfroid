from sangfroid.keyframe import Keyframe
from sangfroid.layer import Group, Field, NamedChildField
from sangfroid.format import Format, Blank
from sangfroid.value.color import Color
from sangfroid.t import T
import bs4
import sangfroid.value as v

@Field.put_in_layer(
        Field('version',          float,       1.2),
        Field('width',            int,         480),
        Field('height',           int,         270),
        Field('xres',             float,       2834.645669),
        Field('yres',             float,       2834.645669),
        Field('gamma-r',          float,       1.0),
        Field('gamma-g',          float,       1.0),
        Field('gamma-b',          float,       1.0),
        Field('view-box',         str, '-4.0 2.25 4.0 -2.25'), # XXX wrong
        Field('antialias',        int,         1), # XXX enum?
        Field('fps',              float,       24.0),
        Field('begin-time',       T,           0),
        Field('end-time',         T,           '5s'),
        Field('active',           bool,        True),
        Field('bgcolor',          str,         '0.5 0.5 0.5 1.0'),

        Field('background_first_color',  v.Color, (0.88, 0.88, 0.88)),
        Field('background_rendering',    v.Integer, 0),
        Field('background_second_color', v.Color, (0.65, 0.65, 0.65)),
        Field('background_size',         v.Dimensions,     (15.0, 15.0)),
        Field('grid_color',              v.Color, (0.623529, 0.623529, 0.623529)),
        Field('grid_show',               v.Integer, 0),
        Field('grid_size',               v.Dimensions, (0.25, 0.25)),
        Field('grid_snap',               v.Integer, 0),
        Field('guide_color',             v.Color, (0.435294, 0.435294, 1.09)),
        Field('guide_show',              v.Integer, 1),
        Field('guide_snap',              v.Integer, 0),
        Field('jack_offset',             v.Real, 0.0),
        Field('onion_skin',              v.Integer, 0),
        Field('onion_skin_future',       v.Integer, 0),
        Field('onion_skin_keyframes',    v.Integer, 1),
        Field('onion_skin_past',         v.Integer, 1),

        NamedChildField('name', doc = """
        The name of this animation.

        Not the filename, though it's often the same.
        """),

        NamedChildField('desc', doc = """
        A description of this animation.

        So you know what it is when you find it again next year.

        Type:
            str or None
        """),

        Group.FIELDS['tag'],
        )
class Animation(Group):
    """
    A Synfig animation.

    Synfig calls this a "canvas", but it also has a layer attribute
    called a "canvas". At first we called it "Sif", but that was
    no good, because it might be loaded from a `.sifz` or `.sfg` file.
    """

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
    def resolution(self):
        """
        The default resolution.

        Type:
            (float, float)
        """
        return (
                float(self._tag.attrs['xres']),
                float(self._tag.attrs['yres']),
                )

    @property
    def viewbox(self):
        """
        The coordinates of the edges of the screen.

        This is a tuple of four floats:
        `(left, bottom, right, top)`.

        (Maybe it would be sensible to have e.g.
        `Animation.top` etc?)

        Type:
            4-tuple of floats
        """
        return tuple([
            float(n) for n in
            self._tag.attrs['view-box'].split(' ')
            ])

    @property
    def fps(self):
        """
        The number of frames per second. Usually 24.

        (Can this be non-integer?)

        Type:
            float
        """
        return float(self._tag.attrs['fps'])
 
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

    @property
    def end_time(self):
        """
        The time at which this animation ends.

        Type:
            T
        """
        return T(self._tag.attrs['end-time'],
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
        print(T(-1, reference_tag=self._tag))
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

    @classmethod
    def _prep_param(cls, f, v):
        # XXX This isn't quite right because something
        # XXX will need to format "content"
        result = bs4.Tag('meta')
        result['name'] = f
        result['content'] = v
        return result
