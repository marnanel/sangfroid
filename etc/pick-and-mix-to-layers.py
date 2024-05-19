import bs4
import json
import sangfroid.value as sv
import sangfroid

# XXX
#  Still to do:
#    - Document all this
#    - Find out about enums by checking through Synfig source
#          See especially
#           synfig-core/src/synfig/paramdesc.cpp
#          and
#           synfig-core/src/synfig/paramdesc.h

OVERRIDES = {
        ('duplicate', 'index'): 'DuplicatesIndexField(None)',
        ('halftone3', 'tone'): 'ParamArrayField(v.Tone)',
}

DEFAULT_SYMBOL = '?'

def tag_children(t):
    result = [p for p in t.children if isinstance(p, bs4.Tag)]
    return result

def main():
    
    with open('etc/layer-details.json', 'r') as f:
        layer_details = json.load(f)

    with open('test/pick-and-mix.sif', 'r') as f:
        soup = bs4.BeautifulSoup(
                f,
                features = 'xml',
                )

    result = ''
    types_done = set()

    for layer in soup.find_all('layer'):
        if layer['type'] in types_done:
            continue
        types_done.add(layer['type'])

        if result:
            result += '\n'

        classname = layer['type'].title()
        details = layer_details.get(classname, None)
        if details:
            symbol = details.get('symbol', DEFAULT_SYMBOL)
        else:
            symbol = DEFAULT_SYMBOL

        result += '@Layer.handles_type()\n'
        result += f'class {layer["type"].title()}(Layer):\n'
        result += '\n'

        result += f'    SYNFIG_VERSION = "{layer["version"]}"\n'
        result += f'    SYMBOL = {repr(symbol)}\n'
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
                    params[paramname] = f'ParamArrayField(v.{typename}, {value})'
                else:
                    params[paramname] = f'ParamTagField(v.{typename}, {value})'
            except NotImplementedError:
                params[paramname] = 'None'
                result += '    raise NotImplementedError()\n'

        for left, right in params.items():
            result += f'    {left:20} = {right}\n'

    print(result)

if __name__=='__main__':
    try:
        main()
    except ValueError as ve:
        print(f'Error: {ve}')
