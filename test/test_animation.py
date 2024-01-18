import os
import sangfroid
from test import *
from bs4 import BeautifulSoup

def test_animation_load_sif():
    sif = get_animation('circles.sif')

    assert sif.name == 'Circles'
    assert sif.description == 'I like circles. They are round.'
    assert sif.size == (480, 270)
    assert sif.resolution==(2834.645669, 2835)
    assert sif.gamma==(0.98, 0.99, 1.0)
    assert sif.background==sangfroid.value.Color('#808080')

def test_animation_load_sifz():
    sif = get_animation('wombats.sifz')

    assert sif.name == 'wombats'
    assert sif.description == 'I like wombats. They live in Australia.'

def strip_spaces(xml):
    # This function used to strip out all space around NavigableStrings
    # and return the changed XML. But that's almost impossible to read
    # in pytest's output. So now it returns a list of:
    #  - for NavigableStrings: the stripped form of item.text
    #           (except that if the stripped form is the empty string,
    #           it's are silently dropped);
    #  - for everything else: lists of name and attributes.

    result = []

    for item in xml.descendants:
        if isinstance(item, bs4.NavigableString):
            s = item.text.strip()
            if s!='':
                result.append(s)
        elif not item.attrs:
            result.append(item.name)
        else:
            addendum = (
                    item.name + ' ' +
                    ' '.join([
                        f'{k}={v}'
                        for k,v
                        in sorted(item.attrs.items())
                        ]))

            result.append(addendum)

    return result

def test_animation_save_and_saveas():

    for test_file in [
            'circles.sif',
            'wombats.sifz',
            ]:

        data = {}

        with open(os.path.join(
            os.path.dirname(__file__),
            test_file,
            ), 'rb') as f:

            original = f.read()

        with open(os.path.join(
            os.path.dirname(__file__),
            f'purple-{test_file}',
            ), 'rb') as f:

            data['expected'] = f.read()

        for save_as in [False, True]:

            tempname = temp_filename()
            with open(tempname, 'wb') as f:
                f.write(original)

            animation = sangfroid.open(tempname)

            for circle in animation.find_all('circle'):
                circle['color'].value = '#ff00ff'

            if save_as:
                final_filename = temp_filename()
                animation.save(final_filename)
            else:
                final_filename = tempname
                animation.save()

            with open(final_filename, 'rb') as f:
                data['found'] = f.read()

            xml = dict(
                    (
                        which,
                        strip_spaces(BeautifulSoup(data[which],
                                                   features='xml')),
                        )
                    for which in ['found', 'expected'])

            assert xml['found']==xml['expected'], (
                    f'test_file, save_as=={save_as}'
                    )

            os.unlink(tempname)
