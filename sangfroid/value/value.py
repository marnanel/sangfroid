import copy
import bs4
import functools
from sangfroid.registry import Registry
from sangfroid.t import T

ANIMATED = 'animated'

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
        return self.tag.name==ANIMATED

    @is_animated.setter
    def is_animated(self, v):
        self._set_animated(v)

    def _set_animated(self, v,
                      adjust_contents = True,
                      ):
        v = bool(v)
        if v==self.is_animated:
            pass
        elif v:

            if adjust_contents:
                former_value = self.value

            our_type = self.tag.name
            self.tag.attrs = {}
            self.tag.name = ANIMATED
            self.tag['type'] = our_type

            if adjust_contents:
                self.tag.clear()
                self.timeline[0] = former_value
        else:
            if adjust_contents:
                timeline = self.timeline
                if len(timeline)==0:
                    first_value = None
                else:
                    first_value = timeline.values()[0].value

            self.tag = bs4.element.Tag(name=self.__class__.__name__.lower())

            if adjust_contents:
                self.value = first_value

    @property
    def timeline(self):
        result = Timeline.__new__(Timeline)
        result.parent = self
        return result

    @timeline.setter
    def timeline(self, v):

        if isinstance(v, list) and all([n for n in v if isinstance(n, Waypoint)]):
            self._set_waypoints(v)
        elif isinstance(v, dict):
            self.timeline = list(v.values())
        elif isinstance(v, Timeline):
            if v.parent is self:
                return
            self._set_waypoints(list(v))
        else:
            raise TypeError("A timeline can only be set to another timeline or "
                            "a dict or list of Waypoints.")

    def _waypoint_tags(self):
        """
        A list of Beautiful Soup tags of waypoints on our timeline.

        The list is in the same order it appears in the file.
        If we're not animated, the list will have no members.

        Returns:
            list of Tag
        """

        if self.tag.name!=ANIMATED:
            return []

        result = [wt for wt in self.tag
                  if isinstance(wt, bs4.element.Tag)]

        return result

    def _waypoints(self):
        """
        A dict of Waypoints on our timeline.

        If we're not animated, the dict will have no members.

        Returns:
            dict mapping T to Waypoint
        """

        waypoints = self._waypoint_tags()

        if not waypoints:
            return {}

        our_type = self.tag['type']

        values = [Waypoint.from_tag(wt,
                                    our_type = our_type,
                                    )
                  for wt in waypoints]

        result = dict([(v.time, v) for v in values])

        return result

    def _set_waypoints(self, v):
        """
        Sets our timeline to contain exactly the given sequence of waypoints.

        They will be stored sorted, with newlines between them.

        This necessarily involves setting ourselves to be animated.

        Args:
            v (list of Waypoints): the waypoints.
        """

        self._set_animated(True,
            adjust_contents = False,
                           )
        self.tag.clear()

        for i, w in enumerate(sorted(v)):
            if i!=0:
                self.tag.append('\n')
            self.tag.append(w.tag)

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
        if result==ANIMATED:
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
    def from_tag(cls, tag,
                 ):

        if tag.name==ANIMATED:

            type_name = tag['type']
            if type_name is None:
                raise ValueError(f"Animated values need a type: {tag}")

        else:
            type_name = tag.name

        result_type = cls.handles_type.from_name(name=type_name)
        result = result_type(tag)

        return result

#######################

class Timeline:
    r"""
    A wrapper for a Value, giving access to its Waypoints.

    This can't be created directly; it should only be created by
    a Value. It holds no state of its own, other than the reference
    to the Value which created it.

    Fields:
        parent (Value): the Value which created this Timeline
    """

    def __init__(self):
        raise NotImplementedError(
                "Don't construct timelines directly."
                )

    def __iter__(self):
        for t in self.parent._waypoint_tags().keys():
            yield t

    def keys(self):
        return list(self.parent._waypoints().keys())

    def values(self):
        return list(self.parent._waypoints().values())

    def items(self):
        return list(self.parent._waypoints().items())

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

    def __getitem__(self, time):
        for t, wt in self.parent._waypoints().items():
            if t==time:
                return wt
            elif t>time:
                return False

        return False

    def __setitem__(self, t, v):

        if isinstance(v, Waypoint):
            new_waypoint = v
        elif isinstance(v, self.parent.__class__):
            new_waypoint = Waypoint(
                    time = t,
                    value = v,
                    reference_tag = self.parent.tag,
                    )
        else:
            new_waypoint = Waypoint(
                    time = t,
                    value = self.parent.__class__(v),
                    reference_tag = self.parent.tag,
                    )

        self.parent.is_animated = True

        waypoints = self.parent._waypoints()

        waypoints[t] = new_waypoint

        self.parent._set_waypoints(waypoints.values())

    def __eq__(self, other):
        if isinstance(other, Timeline):
            return self.values()==other.values()
        else:
            return self.values()==list(other)

    def __str__(self):
        return f'[timeline of {self.parent.__class__.__name__}: {self.parent}]'

    def __len__(self):
        return len(self.keys())

    def __bool__(self):
        return len(self)!=0

    __repr__ = __str__

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
    def __init__(self, time, value, before='clamped', after='clamped',
                 reference_tag = None,
                 ):

        if not isinstance(value, Value):
            raise TypeError(value)

        if value.is_animated:
            raise ValueError("Waypoints can't have animated values")

        if isinstance(time, T):
            self.time = time
        elif isinstance(time, (int, float)):
            self.time = T(time,
                          reference_tag = reference_tag,
                          )
        else:
            raise TypeError(
                    f"time parameter should be T, or numeric: {time}")

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

    @classmethod
    def _check_interpolation_type(cls, v, from_constructor):

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

    @classmethod
    def from_tag(cls, tag,
                 our_type = None,
                 ):
        if tag.name!='waypoint':
            raise ValueError("Waypoints must be called <waypoint>: "
                                f"{tag}")

        try:
            time = T(tag['time'], reference_tag=tag)
        except ValueError:
            raise ValueError(
                    "If a value isn't attached to a document, "
                    "T-values in its timeline must be"
                    "expressed in frames: {tag}"
                    )

        v = [t for t in tag.children if isinstance(t, bs4.element.Tag)]

        if len(v)==0:
            raise ValueError(f"Waypoint without a value: {w}")
        elif len(v)!=1:
            raise ValueError(
                    f"Waypoint with multiple values: {w}")
        elif v[0].name==ANIMATED:
            raise ValueError("Values in waypoints cannot themselves "
                             "be animated")
        elif our_type is not None and v[0].name!=our_type:
            raise ValueError(
                    "Waypoint type must match parent: "
                    f"parent={our_type}, child={v[0].name}")

        result = cls(
                time = time,
                value = Value.from_tag(v[0]),
                before = tag['before'],
                after = tag['after'],
                )

        return result

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        if not isinstance(other, Waypoint):
            return False

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
