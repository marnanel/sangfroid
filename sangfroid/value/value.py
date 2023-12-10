import bs4
from sangfroid.registry import Registry

class Value:

    def __init__(self, *args,
                 timeline = None,
                 ):

        if len(args)==1 and isinstance(args[0], bs4.element.Tag):
            self.tag = args[0]
        else:
            self.tag = self._make_tag_from_args(args)

        assert self.tag is not None

        if timeline is None:
            self._set_value()
        else:
            self._value = Timeline(parent=self)

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
        name = tag.name

        if name!='animated':
            result_type = cls.handles_type.from_name(name=name)
            return result_type(tag)

        waypoints = [w for w in tag.children if isinstance(w, bs4.element.Tag)]

        if len([w for w in waypoints if w.name!='waypoint'])!=0:
                raise ValueError(
                    "Timelines can only contain waypoints. You have: "
                    f"{[w.name for w in waypoints]}")

        timeline = []

        result_type = None

        for waypoint in waypoints:
            values = [v for v in waypoint.children
                      if isinstance(v, bs4.element.Tag)]
            if len(values)==0:
                raise ValueError(
                        f"No value for a waypoint: {w}")
            elif len(values)!=1:
                raise ValueError(
                        f"Multiple values for a waypoint: {w}")

            waypoint_value_tag = values[0]
            waypoint_value = cls.from_tag(waypoint_value_tag)

            if result_type is None:
                result_type = waypoint_value.__class__
            elif not isinstance(waypoint_value, result_type):
                raise ValueError(
                        f"Waypoints are not all of the same type! {tag}")

            assert not waypoint_value.is_animated
            timeline.append([waypoint, waypoint_value])

        result = result_type(tag, timeline=timeline)

        return result

class Timeline:
    def __init__(self, parent):
        self.parent = parent
        self.waypoints = []
        waypoint_tags = [w for w in self.parent.tag
                      if isinstance(w, bs4.element.Tag)]

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
                        value = value,
                        before = waypoint_tag['before'],
                        after = waypoint_tag['before'],
                        ))

class Waypoint:
    def __init__(self, value, before, after):
        # XXX stub
        self.value = value
        self.before = before
        self.after = after
