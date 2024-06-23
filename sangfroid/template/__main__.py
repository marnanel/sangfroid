import bs4
import json
import argparse
import sangfroid.value as sv
import sangfroid
from sangfroid.template.replacer import Replacer
from sangfroid.value.blendmethod import BlendMethod

# XXX
#  Still to do:
#    - Document all this
#    - Merge in the code which reads Synfig source
#    - Load existing classes in order to check for __doc__
#       and inheritance

OVERRIDES = {
        ('duplicate', 'index'): 'f.DuplicatesIndexField(None)',

        # XXX this default is wrong
        ('halftone3', 'tone'): 'f.ParamArrayField(v.Tone, default=None)',
        ('switch', 'canvas'): 'f.SwitchCanvasField()',
}

DEFAULT_SYMBOL = '?'

def parse_args():
    parser = argparse.ArgumentParser(
            description=(
                'convert external things, such as Synfig '
                'sources, to Python code'),
            )
    parser.add_argument(
            '--synfig', type=str,
            default=None,
            help='location of Synfig repo')
    parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='show what\'s being done')
    args = parser.parse_args()
    return args

def tag_children(t):
    result = [p for p in t.children if isinstance(p, bs4.Tag)]
    return result

def main():

    args = parse_args()
    if args.synfig:
        raise ValueError("Still need to merge in the Synfig-checking code")
    
    scan_pick_and_mix(args)

def scan_pick_and_mix(args):
    with open('test/pick-and-mix.sif', 'r') as f:
        soup = bs4.BeautifulSoup(
                f,
                features = 'xml',
                )

    replacer = Replacer(
            verbose = args.verbose,
            )

    types_done = set()

    for layer in soup.find_all('layer'):
        if layer['type'] in types_done:
            continue
        types_done.add(layer['type'])

        result = ''

        classname = layer['type'].title()

        result += f'SYNFIG_VERSION = "{layer["version"]}"\n'
        result += '\n'

        params = {}

        for param in layer.find_all('param'):

            paramname = param['name']
            is_array = False

            if '[' in paramname:
                if '[0]' not in paramname:
                    continue
                paramname = paramname.split('[')[0]
                is_array = True

            override = (layer['type'], paramname)
            if override in OVERRIDES:
                params[paramname] = OVERRIDES[override]

                continue

            c = tag_children(param)

            if c==[] and paramname=='index':
                params['index'] = 'DuplicatesIndexField(None)'
                continue
            elif len(c)>1:
                raise ValueError(f"{paramname} has a strange number of children: {c}")

            value_tag = c[0]

            if paramname=='blend_method':
                typename = 'BlendMethod'
            else:
                typename = value_tag.name.title()

                if typename=='Vector':
                    partnames = sorted([p.name for p in tag_children(value_tag)])
                    if partnames==['x', 'y']:
                        typename = 'X_Y'
                elif typename=='Composite':
                    partnames = sorted([p.name for p in tag_children(value_tag)])
                    if partnames==sorted(sangfroid.value.Transformation.REQUIRED_KEYS):
                        typename = 'Transformation'

            try:
                cls = getattr(sv, typename)
            except AttributeError as ae:
                raise ValueError(
                        f'the layer class {classname} '
                        f'has a param named {paramname} '
                        f'of type {typename}, but that doesn\'t '
                        'appear to exist within synfig.value:\n'
                        f'{ae}')
                return

            try:
                value = cls.from_tag(value_tag).as_python_expression()
                if is_array:
                    params[paramname] = f'f.ParamArrayField(v.{typename}, {value})'
                else:
                    params[paramname] = f'f.ParamTagField(v.{typename}, {value})'
            except NotImplementedError:
                params[paramname] = f'f.NotImplementedField("{typename}")'

        for left, right in params.items():
            if left in (
                    'type',
                    ):
                left += '_'
            result += f'{left:20} = {right}\n'

        replacer.add(classname, result)

    replacer.handle_all_files()
    replacer.check_everything_was_seen()

if __name__=='__main__':
    try:
        main()
    except ValueError as ve:
        print(f'Error: {ve}')
