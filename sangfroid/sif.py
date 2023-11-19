from bs4 import BeautifulSoup
from sangfroid.keyframe import Keyframe
import sangfroid.layer

class Sif(sangfroid.layer.Group):
    def __init__(self, source):
        self.source = source
        with open(self.source, 'r') as f:
            self.soup = BeautifulSoup(
                    f,
                          features = 'xml',
                          )

        assert len(self.soup.contents)==1
        self.main = self.soup.contents[0]
        super().__init__(
                tag = self.main,
                )

    @property
    def name(self):
        return self.main.find('name').string

    @property
    def description(self):
        return self.main.find('desc').string

    @property
    def width(self):
        return int(self.main.attrs['width'])

    @property
    def height(self):
        return int(self.main.attrs['height'])

    @property
    def xres(self):
        return float(self.main.attrs['xres'])

    @property
    def yres(self):
        return float(self.main.attrs['yres'])

    @property
    def gamma(self):
        return (
                float(self.main.attrs['gamma-r']),
                float(self.main.attrs['gamma-g']),
                float(self.main.attrs['gamma-b']),
                )

    @property
    def viewbox(self):
        return tuple([
            float(n) for n in
            self.main.attrs['view-box'].split(' ')
            ])

    @property
    def antialias(self):
        # XXX what is the type?
        return float(self.main.attrs['antialias'])
 
    @property
    def fps(self):
        return float(self.main.attrs['fps'])
 
    @property
    def begin_time(self):
        return self.time_to_frames(self.main.attrs['begin-time'])

    @property
    def end_time(self):
        return self.time_to_frames(self.main.attrs['end-time'])

    @property
    def background(self):
        return tuple([
            float(n) for n in
            self.main.attrs['bgcolor'].split(' ')
            ])

    @property
    def keyframes(self):
        for kf in self.sif.main.find_all('keyframe'):
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
