import copy
import bs4
import functools
from sangfroid.registry import Registry
from sangfroid.t import T
from sangfroid.utils import tag_to_fps, tag_to_canvas_duration

class Value:

    def __init__(self, *args):

        if len(args)==1 and isinstance(args[0], bs4.element.Tag):
            self.tag = args[0]
        else:
            self.tag = bs4.element.Tag(name=self.__class__.__name__.lower())

            if len(args)==1:
                self.value = args[0]
            else:
                self.value = args

        assert self.tag is not None

    @property
    def is_animated(self):
        """
        Whether the value is animated.

        Returns:
            bool
        """
        return self.tag.name=='animated'

    @is_animated.setter
    def is_animated(self, v):
        v = bool(v)
        if v==self.is_animated:
            pass
        elif v:
            our_type = self.tag.name
            self.tag.attrs = {}
            self.tag.name = 'animated'
            self.tag['type'] = our_type
        else:
            self.tag = bs4.element.Tag(name=self.__class__.__name__.lower())
            self.value = None

    def __setitem__(self, t, v):

        self.is_animated = True

        if isinstance(t, T):
            new_time = t
        else:
            try:
                frames = float(t)
            except TypeError:
                raise TypeError(f"Needed T or int or float, not {type(t)}")

            if frames<0:
                frames = tag_to_canvas_duration(self.tag) + frames

            new_time = T(float(frames))

        if isinstance(v, self.__class__):
            new_value = v
        else:
            new_value = self.__class__(v)

        new_waypoint = Waypoint(
                time = new_time,
                value = new_value,
                )

        self.tag.append(new_waypoint.tag)

    """
    @timeline.setter
    def timeline(self, v):
        if v is None:
            self.tag = bs4.element.Tag(name=self.__class__.__name__.lower())
            self.value = None
        elif isinstance(v, list):
            # Run this check before we do anything. Timeline.__iadd__()
            # will check too, but we'll have destroyed the current tag
            # by that time.
            if any([not isinstance(w, Waypoint) for w in v]):
                raise ValueError("Only Waypoints may live in a timeline")

            if self.tag.name!='animated':
                our_type = self.tag.name
                self.tag.attrs = {}
                self.tag.name = 'animated'
                self.tag['type'] = our_type

            self.tag.clear()

            self.timeline += v

        elif isinstance(v, Timeline):
            if v.parent is self:
                return
            self.timeline = list(v)
        else:
            raise TypeError("This can only be set to None or "
                            "a list of Waypoints.")
                            """

    @property
    def timeline():
        raise NotImplementedError() # for now, FIXME

    def _waypoint_tags(self):
        """
        A dict of Beautiful Soup tags of waypoints on our timeline.

        Returns:
            dict mapping T to Tag
        """

        tag = self.tag

        if tag.name!='animated':
            return {}

        try:
            fps = tag_to_fps(tag)
        except ValueError:
            fps = None

        def _construct_time(w):
            try:
                time = T(w['time'], fps)
            except ValueError:
                assert fps is None
                raise ValueError(
                        "If a value isn't attached to a document, "
                        "T-values in its timeline must either be "
                        "expressed in frames or must have the FPS "
                        f"specified explicitly: {tag}"
                        )

        result = dict([
            (_construct_time(w), w)
            for w in tag
            if isinstance(w, bs4.element.Tag)])

        if any([w.name!='waypoint' for w in result.keys()]):
            raise ValueError("Waypoints must all be called <waypoint>: "
                                f"{tag}")

        our_type = tag['type']

        for waypoint_tag in result:
            v = [t for t in waypoint_tag.children
                 if isinstance(t, bs4.element.Tag)]

            if len(v)==0:
                raise ValueError(f"Waypoint without a value: {waypoint_tag}")
            elif len(v)!=1:
                raise ValueError(
                        f"Waypoint with multiple values: {v}")
            elif v[0].name!=our_type:
                raise ValueError(
                        "Waypoint type must match parent: "
                        f"parent={parent_type}, child={v[0].name}")

        return result

    def __iter__(self):
        """
        An iterator over waypoints on our timeline.
        """

        for k,v in sorted(self._waypoint_tags().items()):
            yield time, Waypoint(
                        value = self.from_tag(v[0]),
                        before = waypoint_tag['before'],
                        after = waypoint_tag['after'],
                        )

    def __len__(self):
        return len(self._waypoints())

    @property
    def our_type(self):
        """
        The name of the Synfig layer type.

        For example, 'circle' or 'group'.

        Returns:
            str
        """
        result = self.tag.name
        if result=='animated':
            result = self.tag['type']

        return result

    def _str_inner(self):
        return str(self.value)

    def __str__(self):
        if self.is_animated:
            return '(animated)'
        else:
            return self._str_inner()

    def __repr__(self):
        return '['+self.__class__.__name__+' '+str(self)+']'

    @property
    def value(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, Value):
            return self.value == other.value

        return self.value == other

    ########################

    # Factories, and setup for factories

    handles_type = Registry()

    @classmethod
    def from_tag(cls, tag):

        if tag.name=='animated':

            type_name = tag['type']
            if type_name is None:
                raise ValueError(f"Animated values need a type: {tag}")

        else:
            type_name = tag.name

        result_type = cls.handles_type.from_name(name=type_name)
        result = result_type(tag)

        return result

#######################

"""
class Timeline:
    A wrapper for a Value, giving access to its Waypoints.

    This can't be created directly; it should only be created by
    a Value. It holds no state of its own, other than the reference
    to the Value which created it.

    Fields:
        items (list of Waypoints): the waypoints, in order.
    def __init__(self):
        raise NotImplementedError(
                "Don't construct timelines directly."
                )

    def __iter__(self):
        return iter(self.items)

    def __iter__(self):
        for waypoint in self._waypoints():
            yield waypoint

    def __iadd__(self, waypoints):
        existing = self._waypoints()
        clashes = [
            (old.time, new.time)
                for old in existing
                for new in waypoints
                if old.time==new.time
                ]
        if clashes:
            raise ValueError("There are already Waypoints with those "
                             f"times in this timeline: {clashes}")

        existing.extend(waypoints)

        self.parent.tag.clear()

        for w in sorted(existing):
            self.parent.tag.append(w.tag)

        return self

    def __getitem__(self, index):
        return self._waypoints().__getitem__(index)

    def __setitem__(self, index, value):
        self._waypoints().__getitem__(index, value)

    def __eq__(self, other):
        return list(self)==list(other)

    def __str__(self):
        return f'[timeline of f{self.parent}]'

    __repr__ = __str__
    """

#######################

INTERPOLATION_TYPES = {
        # UI name    SVG name   emoji
        'tcb':      ('auto',     '🟢'),
        'clamped':  ('clamped',  '🔶'),
        'constant': ('constant', '🟥'),
        'linear':   ('linear',   '🌽'), # yeah, I know it's sweetcorn
        'ease':     ('halt',     '🫐'), # blueberry
        'undefined': (None,      '🪨'), # rock
        }

INTERPOLATION_TYPE_SYNONYMS = dict(
        [(v[0], k)
         for k,v in INTERPOLATION_TYPES.items()
         if v[0] is not None])

@functools.total_ordering
class Waypoint:
    def __init__(self, time, value, before='clamped', after='clamped'):

        if not isinstance(value, Value):
            raise TypeError(value)

        if value.is_animated:
            raise ValueError("Waypoints can't have animated values")

        if isinstance(time, T):
            self.time = time
        else:
            raise TypeError(
                    f"time parameter should be T: {time}")

        self._before = self._check_interpolation_type(before, True)
        self._after = self._check_interpolation_type(after, True)
        self.value = value

    @property
    def before(self):
        return self._before

    @before.setter
    def before(self, v):
        self._before = self._check_interpolation_type(v, False)

    @property
    def after(self):
        return self._after

    @after.setter
    def after(self, v):
        self._after = self._check_interpolation_type(v, False)

    def _check_interpolation_type(self, v, from_constructor):

        if v=='undefined':
            if from_constructor:
                raise ValueError(
                        "Waypoints can't have interpolations "
                        "of 'undefined'."
                        )
            else:
                raise ValueError(
                        "You can't set waypoint interpolations "
                        "to 'undefined'."
                        )

        if v in INTERPOLATION_TYPES:
            return v

        if v in INTERPOLATION_TYPE_SYNONYMS:
            return INTERPOLATION_TYPE_SYNONYMS[v]

        raise ValueError(f"Unknown interpolation type: {v}")

    @property
    def tag(self):
        result = bs4.Tag(name="waypoint")
        result['time'] = self.time
        result['before'] = self._before
        result['after'] = self._after
        result.append(
                copy.copy(
                    self.value.tag
                    )
                )
        return result

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        return self.time == other.time

    def __str__(self):
        return '[%3s ' % (self.time,) + (
                f'{INTERPOLATION_TYPES[self.before][1]}-'
                f'{INTERPOLATION_TYPES[self.after][1]} - '
                f'{self.value}]'
                )

    def __getitem__(self, index):
        for k,v in self._waypoints():
            if k==index:
                return v

        raise KeyError(index)

    def __setitem__(self, index):
        for k,v in self._waypoints():
            if k==index:
                return v

        raise KeyError(index)

    __repr__ = __str__

__all__ = [
        'Value',
        'Waypoint',
        ]
