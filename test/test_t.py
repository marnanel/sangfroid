import pytest
import sangfroid
from sangfroid import T
from test import *

TESTS = [
        # "None" in secs means not to look it up.

        # Init param; fps;  frames; secs;  str or exception
        (None,        None,      0,    0,  ValueError), # silly time spec
        ('Banana',    None,      0,    0,  ValueError),
        (2+4j,        None,      0,    0,  ValueError),

        ('0s',        None,      0,    0,  ValueError), # seconds, no fps
        ('2s',        None,      0,    0,  ValueError),

        ('0s',          -1,      0,    0,  ValueError), # silly FPS specs
        ('0s',        24.1,      0,    0,  ValueError),
        ('0s',    'wombat',      0,    0,  ValueError),

        ('0s',          24,      0,    0,  '0f'),       # seconds
        ('2s',          24,     48,    2,  '2s'),
        ('4s',          24,     96,    4,  '4s'),
        ('-2s',         24,    -48,   -2,  '-2s'),
        ('2.5s',        24,     60,  2.5,  '2s 12f'),
        ('-2.5s',       24,    -60, -2.5,  '-2s 12f'),

        ('0s',        None,      0,    0, '0f'),        # s+frames, no fps
        ('0s 2f',     None,      2, 0.08,  ValueError),
        ('2s 2f',     None,      0,    0,  ValueError),

        ('0s 0f',       24,      0,    0,  '0f'),       # seconds + frames
        ('0s 2f',       24,      2, 0.08,  '2f'),
        ('0s 2.5f',     24,    2.5,  0.1,  '2.5f'),
        ('0s 100f',     24,    100, 4.17,  '4s 4f'),
        ('2s 2f',       24,     50, 2.08,  '2s 2f'),
        ('2s -2f',      24,      0,    0,  ValueError),
        ('4s 0f',       24,     96,    4,  '4s'),
        ('-2s -2f',     24,      0,    0,  ValueError),
        ('-2s 2f',      24,    -50,-2.08,  '-2s 2f'),
        ('2.5s 0f',     24,     60,  2.5,  '2s 12f'),
        ('2.5s 2f',     24,     62, 2.58,  '2s 14f'),
        ('2.5s 2.5f',   24,   62.5,  2.6,  '2s 14.5f'),

        ('0f',        None,      0, None,  '0f'),       # frames, no fps
        ('2f',        None,      2, None,  '2f'),
        ('24f',       None,     24, None,  '24f'),
        ('48f',       None,     48, None,  '48f'),
        ('48.5f',     None,   48.5, None,  '48.5f'),
        ('-48.5f',    None,  -48.5, None,  '-48.5f'),

        ('0f',          24,      0,    0,  '0f'),
        ('2f',          24,      2, 0.08,  '2f'),
        ('24f',         24,     24,    1,  '1s'),
        ('48f',         24,     48,    2,  '2s'),
        ('48.5f',       24,   48.5, 2.02,  '2s 0.5f'),
        ('-48.5f',      24,  -48.5,-2.02,  '-2s 0.5f'),

          ]

def test_t_examples():
    for example in TESTS:
        try:
            time = T(example[0], fps=example[1])

            assert round(time.frames, 2)==example[2], (
                    f"frames property: {example}"
                    )
            
            if example[3] is not None:
                assert round(time.seconds, 2)==example[3], (
                    f"seconds property: {example}"
                    )

            assert time == example[2],   f"equal to constant: {example}"
            assert time  < example[2]+1, f"less than constant: {example}"
            assert time  > example[2]-1, f"more than constant: {example}"

            t_same   = T(example[2],   fps=example[1])
            t_before = T(example[2]-1, fps=example[1])
            t_after  = T(example[2]+1, fps=example[1])

            assert time == t_same,   f"equal to another T: {example}"
            assert time != t_before, f"not equal to another T: {example}"
            assert time != t_after,  f"not equal to another T: {example}"
            assert time < t_after,   f"less than another T: {example}"
            assert time > t_before,  f"more than another T: {example}"

            assert hash(time)==hash(t_same),   f"hash equal: {example}"
            assert hash(time)!=hash(t_before), f"hash not equal: {example}"
            assert hash(time)!=hash(t_after),  f"hash not equal: {example}"

            if isinstance(example[4], str):
                assert str(time)==example[4], f"str(): {example}"

            with pytest.raises(AttributeError):
                time.frames = 0

            with pytest.raises(AttributeError):
                time.seconds = 0

            with pytest.raises(AttributeError):
                time.fps = 0

            # (end of the unit tests here)

            assert not isinstance(example[4], Exception), (
                    f"We expected an exception: {example}"
                    )
        except Exception as e:
            if isinstance(e, AssertionError):
                raise

            assert not isinstance(example[4], str), (
                    f"Didn't expect an exception: {example}\n{e}"
                    )
            assert isinstance(e, example[4]), (
                    f"Wrong kind of exception: {example}\n{e}"
                    )

def test_t_no_params():
    zero_t = T()
    assert zero_t.frames==0
    assert zero_t.seconds==0
