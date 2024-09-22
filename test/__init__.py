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

    def munge(n):
        if isinstance(n, bs4.element.Tag):
            pass
        elif isinstance(n, str):
           n = bs4.BeautifulSoup(n, 'xml')
        else:
            raise TypeError(type(n))

        if isinstance(n, bs4.BeautifulSoup):
            n = n.contents[0]

        return n

    a = munge(a)
    b = munge(b)

    assert a.prettify()==b.prettify()

    if asserting is not None:
        if a!=b:
            asserting += f'\na == {a}\nb == {b}'
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
