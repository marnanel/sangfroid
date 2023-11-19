import sangfroid
from test import *

def test_canvas_children():
    sif = get_sif('pick-and-mix.sif')

    found = [str(layer) for layer in sif.descendants]

    assert found==[1]
