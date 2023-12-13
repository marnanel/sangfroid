from bs4 import BeautifulSoup
from sangfroid.keyframe import Keyframe
from sangfroid.layer import Group
from sangfroid.format import Format

class Animation(Group):
    def __init__(self, filename):
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
        return self.tag.find('name').string

    @property
    def description(self):
        return self.tag.find('desc').string

    @property
    def size(self):
        return (
                int(self.tag.attrs['width']),
                int(self.tag.attrs['height']),
                )

    @property
    def resolution(self):
        return (
                float(self.tag.attrs['xres']),
                float(self.tag.attrs['yres']),
                )

    @property
    def gamma(self):
        return (
                float(self.tag.attrs['gamma-r']),
                float(self.tag.attrs['gamma-g']),
                float(self.tag.attrs['gamma-b']),
                )

    @property
    def viewbox(self):
        return tuple([
            float(n) for n in
            self.tag.attrs['view-box'].split(' ')
            ])

    @property
    def antialias(self):
        # XXX what is the type?
        return float(self.tag.attrs['antialias'])
 
    @property
    def fps(self):
        return float(self.tag.attrs['fps'])
 
    @property
    def begin_time(self):
        return self.time_to_frames(self.tag.attrs['begin-time'])

    @property
    def end_time(self):
        return self.time_to_frames(self.tag.attrs['end-time'])

    @property
    def background(self):
        return tuple([
            float(n) for n in
            self.tag.attrs['bgcolor'].split(' ')
            ])

    @property
    def keyframes(self):
        for kf in self.sif.tag.find_all('keyframe'):
            yield Keyframe.from_tag(kf)
 
    @property
    def contents(self):
        yield 'no'

    def time_to_frames(self, t):
        if ' ' in t:
            return sum([self.time_to_frames(n) for n in t.split(' ')])

        if t.endswith('s'):
            return int(float(t[:-1])*self.fps)
        elif t.endswith('f'):
            return int(t[:-1])
        else:
            raise ValueError(f"I don't understand the time specification: {t}")

def open(filename):
    """
    Loads the Synfig file with the given filename.

    Args:
        filename (str): the name of the source file. Can be .sfg, .sif,
            or .sifz.

    Returns:
        Animation
    """
    result = Animation(filename)
    return result
