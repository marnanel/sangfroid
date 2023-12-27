import pytest
import sangfroid
from sangfroid.value import *
from test import *

def test_gradient_simple():
    sif = get_animation('pick-and-mix.sif')
    mandelbrot = sif.find(type='mandelbrot')
    g = mandelbrot['gradient_inside']

    assert len(g)==2
    assert all([isinstance(c, Color) for c in g])
    assert str(g[0])=='#ff0000'
    assert str(g[1])=='#ffff00'
    assert str(g)=='[#ff0000,#ffff00]'
    assert repr(g)=='[Gradient [#ff0000,#ffff00]]'

    blue = Color('#0000ff')
    g[1] = blue
    assert str(g[0])=='#ff0000'
    assert str(g[1])=='#0000ff'
    assert str(g)=='[#ff0000,#0000ff]'
    assert repr(g)=='[Gradient [#ff0000,#0000ff]]'
