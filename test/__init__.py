import os
import logging
import sangfroid
import tempfile
import bs4
import xml.sax

logger = logging.getLogger('sangfroid.test')

def get_animation(name):
    filename = os.path.join(
            os.path.dirname(__file__),
            name,
            )

    return sangfroid.open(filename)

def xml_compare(a, b,
                asserting=None):

    class Comparer(xml.sax.ContentHandler):
        """
        this is baroque, but allows us to normalise
        self-closing tags easily
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__lines = []

        def startElement(self, name, attrs):
            s = f'<{name}' + (
                    ' '.join([f"{k}={v}" for k,v in attrs.items()])
                    ) + '>'
            self.__lines.append(s)

        def endElement(self, name):
            s = f'</{name}>'
            self.__lines.append(s)

        def characters(self, content):
            if content.strip()=='':
                return
            self.__lines.append(content)

        @property
        def lines(self):
            return self.__lines

    def munge(n):
        if isinstance(n, bs4.element.Tag):
            pass
        elif isinstance(n, str):
           n = bs4.BeautifulSoup(n, 'xml')
        else:
            raise TypeError(type(n))

        comparer = Comparer()
        xml.sax.parseString(
                string = str(n),
                handler = comparer,
                )
        
        return comparer.lines

    a = munge(a)
    b = munge(b)

    if asserting is not None:
        if a!=b:
            for aa,bb in zip(a,b):
                asserting += f'\n{aa:40} {bb}'
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
