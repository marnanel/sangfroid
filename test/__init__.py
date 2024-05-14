import os
import logging
import sangfroid
import tempfile
import bs4

logger = logging.getLogger('sangfroid.test')

def get_animation(name):
    filename = os.path.join(
            os.path.dirname(__file__),
            name,
            )

    return sangfroid.open(filename)

def xml_compare(a, b,
                asserting=None):

    def normalise(n):
        if isinstance(n, bs4.element.Tag):
            return n
        elif isinstance(n, str):
            return bs4.BeautifulSoup(n, 'xml')
        else:
            raise TypeError(type(n))

    def munge(n):
        result = normalise(n).prettify()

        if result.startswith('<?xml'):
            result = result.split('\n', 1)[1]

        return result

    a = munge(a)
    b = munge(b)

    if asserting is not None:
        assert a==b, asserting
    else:
        return a==b

def temp_filename(
        suffix = '.sif',
        ):
    fd, tempname = tempfile.mkstemp(
            prefix='sangfroid',
            suffix=suffix,
            )
    os.close(fd)
    return tempname
