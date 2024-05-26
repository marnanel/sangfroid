from test import *
import pytest
from sangfroid.layer.layer import Layer
import sangfroid.layer.field as f
import sangfroid.value as v
from bs4 import BeautifulSoup

class Wombat(Layer):
    SYMBOL = '⭐'

    SYNFIG_VERSION = "0.1"
    z_depth              = f.ParamTagField(v.Real, 0.0)
    bline                = f.NotImplementedField("Bline")

def test_notimplementedfield():
    tag = BeautifulSoup("""<layer type="wombat" active="true"
    exclude_from_rendering="false" version="0.1">
    <param name="z-depth">
        <real value="1.0"/>
    </param>
    <bline name="bline">
        <is_this_implemented answer="no of course not"/>
    </bline>
    </layer>""",
                        features='xml',
                        )

    # Instantiating the class works...
    wombat = Wombat(tag)

    # So does accessing z_depth...
    assert wombat.z_depth==1.0
    wombat.z_depth = 2.0
    assert wombat.z_depth==2.0

    # But reading from bline will fail
    with pytest.raises(NotImplementedError):
        bline = wombat.bline

    # So will writing to it
    with pytest.raises(NotImplementedError):
        wombat.bline = 'My old man\'s a dustman'
