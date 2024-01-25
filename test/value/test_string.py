import pytest
import sangfroid
from test import *

def test_string_read():
    sif = get_animation('pick-and-mix.sif')
    drop = sif.find(desc='drop.png')
    assert drop['filename']=='drop.png'

def test_string_write():
    sif = get_animation('pick-and-mix.sif')
    drop = sif.find(desc='drop.png')
    assert drop['filename']=='drop.png'
    drop['filename'] = 'wombat.png'
    assert drop['filename']=='wombat.png'
