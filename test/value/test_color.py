import pytest
import sangfroid
from sangfroid.value import *
from test import *

def test_value_color_compare():
    sif = get_animation('circles.sif')

    blue_circle = sif.find(desc='Blue circle')
    found = blue_circle['color']

    LITERALS = [
            ('tuple, with alpha',    (0.0, 0.2, 1.0, 1.0)),
            ('tuple, no alpha',      (0.0, 0.2, 1.0)),
            ('string, with alpha',   '#0033FFFF'),
            ('string, no alpha',     '#0033FF'),
            ]

    OBJECTS = [('retrieved from sif', found)]
    OBJECTS.extend([
        (f'colour from {name}', Color(o))
        for name, o in LITERALS])

    for first_name, first in OBJECTS:
        for literal_name, literal in LITERALS:
            assert first==literal, f"{first_name} vs {literal_name}"

        for second_name, second in OBJECTS:
            assert first==second, f"{first_name} vs {second_name}"

def test_value_color_assign():
    c = Color()
    xml_compare(c.tag, """
<color>
  <r>1.000000</r>
  <g>1.000000</g>
  <b>1.000000</b>
  <a>1.000000</a>
</color>""", asserting='with no parameters')

    c = Color(0.1, 0.2, 0.3)
    xml_compare(c.tag, """
<color>
  <r>0.100000</r>
  <g>0.200000</g>
  <b>0.300000</b>
  <a>1.000000</a>
</color>""", asserting='with 3 floats')

    c = Color(0.1, 0.2, 0.3, 0.4)
    xml_compare(c.tag, """
<color>
  <r>0.100000</r>
  <g>0.200000</g>
  <b>0.300000</b>
  <a>0.400000</a>
</color>""", asserting='with 4 floats')

    c = Color("#102030")
    xml_compare(c.tag, """
<color>
  <r>0.062745</r>
  <g>0.125490</g>
  <b>0.188235</b>
  <a>1.000000</a>
</color>""", asserting='with 6 hex digits with hash')

    c = Color("102030")
    xml_compare(c.tag, """
<color>
  <r>0.062745</r>
  <g>0.125490</g>
  <b>0.188235</b>
  <a>1.000000</a>
</color>""", asserting='with 6 hex digits with no hash')

    c = Color("#10203040")
    xml_compare(c.tag, """
<color>
  <r>0.062745</r>
  <g>0.125490</g>
  <b>0.188235</b>
  <a>0.250980</a>
</color>""", asserting='with 8 hex digits with hash')

    c = Color("10203040")
    xml_compare(c.tag, """
<color>
  <r>0.062745</r>
  <g>0.125490</g>
  <b>0.188235</b>
  <a>0.250980</a>
</color>""", asserting='with 8 hex digits with no hash')
