import sangfroid
from sangfroid.value.value import Waypoint
from sangfroid.time import Time
from test import *
import pytest

def test_waypoint_simple():
    sif = get_sif('bouncing.sif')

    ball = sif.find(desc='Ball')
    scale = ball['transformation']['scale']

    assert scale.is_animated

    for found, expected in zip(scale.timeline, [
        ( '0f', 'ease', 'ease'),
        ('24f', 'linear', 'linear'),
        ('48f', 'ease', 'ease'),
        ]):

        assert found.time==Time(expected[0])
        assert found.before==expected[1]
        assert found.after==expected[2]

def test_waypoint_interpolation_types():

    value = sangfroid.value.Bool(True)

    for source_type, expected_type, expected_emoji in [
            ('auto',     'tcb',      '🟢'),
            ('tcb',      'tcb',      '🟢'),
            ('clamped',  'clamped',  '🔶'),
            ('constant', 'constant', '🟥'),
            ('linear',   'linear',   '🌽'),
            ('ease',     'ease',     '🫐'),
            ('halt',     'ease',     '🫐'),
            ]:
        waypoint = Waypoint('0f', source_type, source_type, value)

        assert waypoint.before == expected_type, source_type
        assert waypoint.after  == expected_type, source_type

        found_emoji = str(waypoint).split(' ')[2]
        assert found_emoji == f'{expected_emoji}-{expected_emoji}'

    with pytest.raises(ValueError):
        Waypoint('0f', 'undefined', 'auto', value)

def test_waypoint_silly():

    value = sangfroid.value.Bool(True)

    with pytest.raises(ValueError):
        # silly interpolation type
        Waypoint('0f', 'wombat', 'ease', value)

    with pytest.raises(TypeError):
        # values must be sangfroid.value.Values
        Waypoint('0f', 'ease', 'ease', True)

def test_waypoint_time_spec():
    value = sangfroid.value.Bool(True)
    w1 = Waypoint('20f', 'ease', 'ease', value)
    w2 = Waypoint(20, 'ease', 'ease', value)
    w3 = Waypoint(Time('20f'), 'ease', 'ease', value)

    assert w1==w2
    assert w1==w3
    assert w2==w3

    with pytest.raises(ValueError):
        Waypoint('bananas', 'ease', 'ease', value)

    with pytest.raises(TypeError):
        Waypoint(None, 'ease', 'ease', value)
