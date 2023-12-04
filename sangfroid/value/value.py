import bs4
from sangfroid.registry import Registry

class Value:

    def __init__(self, tag,
                 timeline = None,
                 ):

        self.tag = tag
        self._timeline = timeline

        if timeline is None:
            self._set_value()

        assert hasattr(self, '_value')

    @property
    def is_animated(self):
        return self._timeline is not None

    def __str__(self):
        if self._timeline is None:
            return str(self.value)
        else:
            return '(animated)'

    def __repr__(self):
        return '['+self.__class__.__name__+' '+str(self)+']'

    @property
    def value(self):
        if self._timeline is not None:
            raise ValueError("This value is animated.")
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

            assert waypoint_value._timeline is None
            timeline.append([waypoint, waypoint_value])

        result = result_type(tag, timeline=timeline)

        return result
