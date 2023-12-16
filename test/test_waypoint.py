import sangfroid
from sangfroid.value.value import Waypoint
from sangfroid.t import T
from test import *
import pytest

def test_waypoint_loaded():
    sif = get_animation('bouncing.sif')

    ball = sif.find(desc='Ball')
    scale = ball['transformation']['scale']

    assert scale.is_animated

    for found, expected in zip(scale.timeline, [
        ( '0f', 'ease', 'ease'),
        ('24f', 'linear', 'linear'),
        ('48f', 'ease', 'ease'),
        ]):

        assert found.time==T(expected[0])
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
        waypoint = Waypoint(T('0f'), value=value,
                            before=source_type, after=source_type)

        assert waypoint.before == expected_type, source_type
        assert waypoint.after  == expected_type, source_type

        found_emoji = str(waypoint).split(' ')[2]
        assert found_emoji == f'{expected_emoji}-{expected_emoji}'

    with pytest.raises(ValueError):
        Waypoint(time=T('0f'), value=value, before='undefined', after='auto')

def test_waypoint_silly():

    value = sangfroid.value.Bool(True)

    with pytest.raises(ValueError):
        # silly interpolation type
        Waypoint(time=T('0f'), value=value, before='wombat', after='ease')

    with pytest.raises(TypeError):
        # values must be sangfroid.value.Values
        Waypoint(time=T('0f'), value=True)

def test_waypoint_time_spec():
    value = sangfroid.value.Bool(True)
    w1 = Waypoint(time=T('20f'), value=value)
    assert int(w1.time)==20

    with pytest.raises(TypeError):
        Waypoint(time='bananas', value=value)

    with pytest.raises(TypeError):
        Waypoint(time=None, value=value)
