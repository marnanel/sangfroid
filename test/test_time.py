import sangfroid
from sangfroid.time import Time
from test import *

def test_time_seconds():
    t = Time('0s')
    assert int(t)==0
    assert t.frames==0
    assert t.seconds==0.0
    assert str(t)=='0f'

    t = Time('2s')
    assert int(t)==48
    assert t.frames==48
    assert t.seconds==2.0
    assert str(t)=='48f'

    t = Time('2s', fps=40)
    assert int(t)==80
    assert t.frames==80
    assert t.seconds==2.0
    assert str(t)=='80f'

def test_time_frames():
    t = Time('0f')
    assert int(t)==0
    assert t.frames==0
    assert t.seconds==0.0
    assert str(t)=='0f'

    t = Time('48f')
    assert int(t)==48
    assert t.frames==48
    assert t.seconds==2.0
    assert str(t)=='48f'

    t = Time('80f', fps=40)
    assert int(t)==80
    assert t.frames==80
    assert t.seconds==2.0
    assert str(t)=='80f'

def test_time_frames_as_int():
    t = Time(0)
    assert int(t)==0
    assert t.frames==0
    assert t.seconds==0.0
    assert str(t)=='0f'

    t = Time(48)
    assert int(t)==48
    assert t.frames==48
    assert t.seconds==2.0
    assert str(t)=='48f'

    t = Time(80, fps=40)
    assert int(t)==80
    assert t.frames==80
    assert t.seconds==2.0
    assert str(t)=='80f'
