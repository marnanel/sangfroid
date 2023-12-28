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

def test_gradient_constructor():
    g = Gradient({0.1: Color('#ff00ff'), 0.7: Color('#ffffff')})
    assert str(g.tag)==(
            '<gradient>'
            '<color pos="0.1"><r>1.000000</r><g>0.000000</g>'
            '<b>1.000000</b><a>1.000000</a></color>'
            '<color pos="0.7"><r>1.000000</r><g>1.000000</g>'
            '<b>1.000000</b><a>1.000000</a></color>'
            '</gradient>'
            )

def test_gradient_assign_dict():
    sif = get_animation('pick-and-mix.sif')
    mandelbrot = sif.find(type='mandelbrot')
    g = mandelbrot['gradient_inside']

    assert g.value=={0.0: Color('#ff0000'), 1.0: Color('#ffff00')}

    g.value = {0.1: Color('#ff00ff'), 0.7: Color('#ffffff')}
    assert g.value=={0.1: Color('#ff00ff'), 0.7: Color('#ffffff')}

def test_gradient_assign_another_gradient():
    sif = get_animation('pick-and-mix.sif')
    mandelbrot = sif.find(type='mandelbrot')
    g1 = mandelbrot['gradient_inside']

    assert g1.value=={0.0: Color('#ff0000'), 1.0: Color('#ffff00')}

    g2 = Gradient({0.1: Color('#ff00ff'), 0.7: Color('#ffffff')})
    assert g2.value=={0.1: Color('#ff00ff'), 0.7: Color('#ffffff')}

    g1.q = g2
    a = dict(g2.value)
    g1.value = dict(a)#g2.value
    assert g1.value=={0.1: Color('#ff00ff'), 0.7: Color('#ffffff')}
    assert g1.value==g2.value
    assert mandelbrot['gradient_inside']==g2.value
