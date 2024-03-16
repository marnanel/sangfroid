from bs4 import BeautifulSoup
from sangfroid.keyframe import Keyframe
from sangfroid.layer import Group
from sangfroid.format import Format
from sangfroid.value.color import Color
from sangfroid.t import T
from sangfroid.utils import tag_to_canvas_duration

class Animation(Group):
    """
    A Synfig animation.

    Synfig calls this a "canvas", but it also has a layer attribute
    called a "canvas". At first we called it "Sif", but that was
    no good, because it might be loaded from a `.sifz` or `.sfg` file.

    At present there's no way to create a new, blank canvas.
    You have to create one in Synfig Studio first.
    This will be fixed soon.

    Most of the properties don't yet have setters. They will.
    """
    def __init__(self, filename:str):
        """
        Args:
            filename: the name of the main file to load.
        """
        self.filename = filename
        self.format = Format.from_filename(filename)

        with self.format.main_file() as f:
            self.soup = BeautifulSoup(
                    f,
                    features = 'xml',
                    )

        assert len(self.soup.contents)==1
        tag = self.soup.contents[0]
        super().__init__(
                tag = tag,
                )

    @property
    def name(self):
        """
        The name of this animation.

        Not the filename, though it's often the same.
        """
        return self.tag.find('name').string

    @property
    def description(self):
        """
        A description of this animation.

        So you know what it is when you find it again next year.

        Type:
            str
        """
        return self.tag.find('desc').string

    @property
    def size(self):
        """
        The height and width of the screen.

        Type:
            (int, int)
        """
        return (
                int(self.tag.attrs['width']),
                int(self.tag.attrs['height']),
                )

    @property
    def resolution(self):
        """
        The default resolution.

        Type:
            (float, float)
        """
        return (
                float(self.tag.attrs['xres']),
                float(self.tag.attrs['yres']),
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
            self.tag.attrs['view-box'].split(' ')
            ])

    @property
    def fps(self):
        """
        The number of frames per second. Usually 24.

        (Can this be non-integer?)

        Type:
            float
        """
        return float(self.tag.attrs['fps'])
 
    @property
    def begin_time(self):
        """
        The time at which this animation starts.

        Almost always zero.

        Type:
            T
        """
        return T(self.tag.attrs['begin-time'],
                 fps=self.fps,
                 )

    @property
    def end_time(self):
        """
        The time at which this animation ends.

        Type:
            T
        """
        return T(self.tag.attrs['end-time'],
                 fps=self.fps,
                 )

    def __len__(self):
        """
        The number of frames in this animation.

        Should be equal to `int(end_time)-int(begin_time)`.

        Type:
            int
        """
        return tag_to_canvas_duration(self.tag)

    @property
    def background(self):
        """
        The background colour.

        Type:
            Color
        """
        triplet = tuple([
            float(n) for n in
            self.tag.attrs['bgcolor'].split(' ')
            ])
        result = Color(*triplet)
        return result

    @property
    def keyframes(self):
        """
        The defined keyframes.

        This is subject to change. At present it's just a generator
        over the keyframes. But the keyframe collection needs to be
        a class in itself, so you can add and delete them.
        """
        for kf in self.sif.tag.find_all('keyframe'):
            yield Keyframe.from_tag(kf)
 
    def save(self, filename:str=None):
        """
        Saves the animation back out to disk.

        Args:
            filename: the filename to save the animation to.
                If None, we use the filename we loaded it from.
        """
        self.format.save(
                content = self.soup,
                filename = filename,
                )
