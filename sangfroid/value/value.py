import bs4
import functools
from sangfroid.registry import Registry
from sangfroid.time import Time

class Value:

    def __init__(self, *args,
                 timeline = None,
                 ):


        if len(args)==1 and isinstance(args[0], bs4.element.Tag):
            self.tag = args[0]
        else:
            self.tag = self._make_tag_from_args(args)

        assert self.tag is not None

        if timeline is None and self.tag.name!='animated':
            self._set_value()
        else:
            self._value = Timeline(parent=self,
                                   literal = timeline,
                                   )

        assert hasattr(self, '_value')

    @property
    def is_animated(self):
        return isinstance(self._value, Timeline)

    @property
    def timeline(self):
        if isinstance(self._value, Timeline):
            return self._value
        return None

    def _make_tag_from_value(self, value):
        raise NotImplementedError(
                f"{self.__class__.__name__} can't yet be initialised "
                "with a literal value."
                )

    def __str__(self):
        if self.is_animated is None:
            return str(self.value)
        else:
            return '(animated)'

    def __repr__(self):
        return '['+self.__class__.__name__+' '+str(self)+']'

    @property
    def value(self):
        if isinstance(self._value, Timeline):
            return None
        return self._value

    def __eq__(self, other):
        if isinstance(other, Value):
            return self.value == other.value


        return other == self._value

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

class Timeline:
    def __init__(self,
                 parent,
                 literal = None,
                 ):
        self.parent = parent
        self.waypoints = []
        waypoint_tags = [w for w in self.parent.tag
                      if isinstance(w, bs4.element.Tag)]

        if literal is not None:
            if waypoint_tags:
                raise ValueError(
                        f"You can't create a timeline on {parent.tag}, "
                        "because it already has a timeline in the file.")
            if any([not isinstance(w, Waypoint) for w in literal]):
                raise TypeError(
                        "Everything in a timeline must be a Waypoint: "
                        f"{literal}")
            self.waypoints = list(literal)
            return

        if any([w.name!='waypoint' for w in waypoint_tags]):
            raise ValueError("Waypoints must all be called <waypoint>: "
                                f"{self.parent.tag}")

        parent_type = self.parent.tag['type']

        for waypoint_tag in waypoint_tags:
            v = [t for t in waypoint_tag.children
                 if isinstance(t, bs4.element.Tag)]

            if len(v)==0:
                raise ValueError(f"Waypoint without a value: {waypoint_tag}")
            elif len(v)!=1:
                raise ValueError(
                        f"Waypoint with multiple values: {v}")
            elif v[0].name!=parent_type:
                raise ValueError(
                        "Waypoint type must match parent: "
                        f"parent={parent_type}, child={v[0].name}")

            value = self.parent.from_tag(v[0])
            self.waypoints.append(
                    Waypoint(
                        time = Time(waypoint_tag['time']),
                        value = value,
                        before = waypoint_tag['before'],
                        after = waypoint_tag['after'],
                        ))

    def __iter__(self):
        for waypoint in sorted(self.waypoints):

            # Check the value isn't animated, just in case
            # someone's managed to change it on the fly
            assert not waypoint.value.is_animated

            yield waypoint

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
    def __init__(self, time, before, after, value):

        if not isinstance(value, Value):
            raise TypeError(value)

        if value.is_animated:
            raise ValueError("Waypoints can't have animated values")

        self.time = time
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

    __repr__ = __str__
