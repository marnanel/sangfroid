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
    assert list(g.keys())==[0.0, 1.0]
    assert list(g.values())==[Color('#ff0000'), Color('#ffff00')]
    assert list(g.items())==[(0.0, Color('#ff0000')), (1.0, Color('#ffff00'))]
    assert str(g)=='{0.0:#ff0000,1.0:#ffff00}'
    assert repr(g)=='[Gradient {0.0:#ff0000,1.0:#ffff00}]'

def test_gradient_setitem():
    sif = get_animation('pick-and-mix.sif')
    mandelbrot = sif.find(type='mandelbrot')
    g = mandelbrot['gradient_inside']

    blue = Color('#0000ff')
    g[1] = blue
    assert str(g[0])=='#ff0000'
    assert str(g[1])=='#0000ff'
    assert str(g)=='{0.0:#ff0000,1.0:#0000ff}'
    assert repr(g)=='[Gradient {0.0:#ff0000,1.0:#0000ff}]'
