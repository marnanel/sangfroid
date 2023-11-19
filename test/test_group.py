import sangfroid
from test import *

def test_canvas_children():
    sif = get_sif('circles.sif')

    EXPECTED = [
            "[🔵circle 'Red circle']",
            "[📂group 'More circles']",
            "[📂group 'Blurry circle']",
            ]

    found = [str(layer) for layer in sif.children]

    assert found==EXPECTED

def test_canvas_descendants():
    sif = get_sif('circles.sif')

    EXPECTED = [
            "[🔵circle 'Red circle']",
            "[📂group 'More circles']",
            "[-🔵circle 'Yellow circle']",
            "[-📂group 'All right, one more circle']",
            "[-🔵circle 'Orange circle']",
            "[📂group 'Blurry circle']",
            "[-🟠blur 'Blur']",
            "[-🔵circle 'Blue circle']",
            ]

    found = [str(layer) for layer in sif.descendants]

    assert found==EXPECTED
