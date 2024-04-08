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

        (0,             24,      0,    0,  '0f'),
        (1,             24,      1, 0.04,  '1f'),
        (2,             24,      2, 0.08,  '2f'),
        (-1,            24,    120, 5.00,  '5s'),
        (-2,            24,    119, 4.96,  '4s 23f'),

          ]

def test_t_examples():

    sif = get_animation('bouncing.sif')

    for example in TESTS:
        try:

            if example[1] is None:
                tag = None
            else:
                sif.tag['fps'] = str(example[1])
                tag = sif.tag

            time = T(example[0], reference_tag=tag)

            message = (
                    "\n"
                    f"Constructor argument: {repr(example[0])}\n"
                    f"            with FPS: {example[1]}\n"
                    )

            if isinstance(example[4], str):
                message += (
                        f"    gives a value of: "
                        f"{example[2]}s {example[3]}f\n"
                        f"which stringifies to: {example[4]}\n"
                        )
            else:
                message += (
                        f"        should raise: {example[4]}\n"
                        )

            assert round(time.frames, 2)==example[2], (
                    f"frames property: {message}"
                    )
            
            if example[3] is not None:
                assert round(time.seconds, 2)==example[3], (
                    f"seconds property: {message}"
                    )

            assert time == example[2],   f"equal to constant: {message}"
            assert time  < example[2]+1, f"less than constant: {message}"
            assert time  > example[2]-1, f"more than constant: {message}"

            t_same   = T(f'{example[2]}f',   reference_tag=tag)
            t_before = T(f'{example[2]-1}f', reference_tag=tag)
            t_after  = T(f'{example[2]+1}f', reference_tag=tag)

            assert time == t_same,   f"equal to another T: {message}"
            assert time != t_before, f"not equal to another T: {message}"
            assert time != t_after,  f"not equal to another T: {message}"
            assert time < t_after,   f"less than another T: {message}"
            assert time > t_before,  f"more than another T: {message}"

            assert hash(time)==hash(t_same),   f"hash equal: {message}"
            assert hash(time)!=hash(t_before), f"hash not equal: {message}"
            assert hash(time)!=hash(t_after),  f"hash not equal: {message}"

            if isinstance(example[4], str):
                assert str(time)==example[4], f"str(): {message}"

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
