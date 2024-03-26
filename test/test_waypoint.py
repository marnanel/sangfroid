import sangfroid
from sangfroid.value.value import Waypoint
from sangfroid.value import Real, Angle
from sangfroid.t import T
from test import *
import bs4
import pytest

def test_waypoint_loaded():
    sif = get_animation('bouncing.sif')

    ball = sif.find(desc='Ball')
    angle = ball['transformation']['angle']

    assert not angle.is_animated
    assert angle.timeline==[]
    assert not angle.timeline
    assert len(angle.timeline)==0

    scale = ball['transformation']['scale']

    assert scale.is_animated
    assert scale.timeline!=[]
    assert scale.timeline
    assert len(scale.timeline)==3

    for found, expected in zip(scale.timeline.values(), [
        ( '0f', 'ease', 'ease'),
        ('24f', 'linear', 'linear'),
        ('48f', 'ease', 'ease'),
        ]):

        assert found.time==T(expected[0])
        assert found.before==expected[1]
        assert found.after==expected[2]

def test_value_set_is_animated():
    sif = get_animation('bouncing.sif')
    
    ball = sif.find(desc='Ball')
    angle = ball['transformation']['angle']

    assert not angle.is_animated
    angle.is_animated = True
    assert angle.is_animated
    angle.timeline[T('1s')] = Angle(90)

    angle.is_animated = False
    assert not angle.is_animated


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

    with pytest.raises(ValueError):
        Waypoint(time='bananas', value=value)

    with pytest.raises(TypeError):
        Waypoint(time=None, value=value)

def test_waypoint_add():
    sif = get_animation('bouncing.sif')
    assert len(sif)==121

    ball = sif.find(desc='Bouncy ball')
    color = ball['color']
    assert not color.is_animated

    color.timeline[0] = '#FF0000'
    color.timeline[16] = '#00FF00'
    color.timeline[32] = '#0000FF'
    color.timeline[47] = '#FF0000'

    sif.save('/tmp/flashy.sif')

    waypoint_details = [str(c) for c in color.tag.children
                        if isinstance(c, bs4.Tag)]

    assert waypoint_details == [
            ('<waypoint after="clamped" before="clamped" time="0f"><color>'
             '<r>1.000000</r><g>0.000000</g><b>0.000000</b><a>1.000000</a>'
             '</color></waypoint>'),
            ('<waypoint after="clamped" before="clamped" time="16f"><color>'
             '<r>0.000000</r><g>1.000000</g><b>0.000000</b><a>1.000000</a>'
             '</color></waypoint>'),
            ('<waypoint after="clamped" before="clamped" time="1s 8f"><color>'
             '<r>0.000000</r><g>0.000000</g><b>1.000000</b><a>1.000000</a>'
             '</color></waypoint>'),
            ('<waypoint after="clamped" before="clamped" time="1s 23f"><color>'
             '<r>1.000000</r><g>0.000000</g><b>0.000000</b><a>1.000000</a>'
             '</color></waypoint>'),
            ]

def test_value_timeline_assign_once():
    r = Real(1.77)
    assert str(r)=='1.77'

    r.timeline = [
            Waypoint(time=T('0f'), value=Real(1.0)),
            Waypoint(time=T('1f'), value=Real(2.0)),
            ]

    s = Real(1.77)
    s.timeline = r.timeline

    for obj in [r, s]:
        assert [str(w.value) for w in obj.timeline] == ['1.0', '2.0']

    assert r.timeline[0] == s.timeline[0]
    assert r.timeline[0] is not s.timeline[0]

def test_value_timeline_assign_twice():
    r = Real(1.77)
    assert str(r)=='1.77'
    assert r.is_animated == False

    r.timeline = [
            Waypoint(time=T('0f'), value=Real(1.0)),
            ]
    assert r.is_animated == True
    assert len(r.timeline)==1
    assert r.timeline[0].time == T('0f')
    with pytest.raises(KeyError):
        r.timeline[1]

    r.timeline = [
            Waypoint(time=T('1f'), value=Real(2.0)),
            ]
    assert r.is_animated == True
    assert len(r.timeline)==1
    with pytest.raises(KeyError):
        r.timeline[0]
    assert r.timeline[1].time == T('1f')

def test_value_is_animated():
    sif = get_animation('bouncing.sif')

    ball = sif.find(desc='Ball')
    scale = ball['transformation']['scale']

    assert scale.is_animated
    original_point_0 = scale.timeline[0].value

    scale.is_animated = False
    assert not scale.is_animated
    assert scale==original_point_0

    scale.is_animated = True
    assert scale.is_animated
    assert scale.timeline[0].value==original_point_0
