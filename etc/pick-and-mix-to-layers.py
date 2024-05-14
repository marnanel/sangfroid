import bs4

# XXX
#  Still to do:
#    - Read default types out of pick-and-mix (will need
#       s.v.Value subclasses)
#       -- this will involve writing s.v.Value subclasses
#           for the weirder ones
#    - Add list of known layer types.
#       -- it should include their existing symbols.
#    - Find out about enums by checking through Synfig source

OVERRIDES = {
        ('duplicate', 'index'): 'DuplicatesIndexField(None)',
        ('halftone3', 'tone'): 'ParamArrayField(v.Tone)',
}

def tag_children(t):
    result = [p for p in t.children if isinstance(p, bs4.Tag)]
    return result

def main():
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

        result += f'class {layer["type"].title()}(Layer):\n'
        result += '\n'

        result += f'    SYNFIG_VERSION = {layer["version"]}\n'
        result += '\n'

        params = {}

        for param in layer.find_all('param'):

            param_name = param['name']
            is_array = False

            if '[' in param_name:
                if '[0]' not in param_name:
                    continue
                param_name = param_name.split('[')[0]
                is_array = True

            override = (layer['type'], param_name)
            if override in OVERRIDES:
                params[param_name] = OVERRIDES[override]

                continue

            c = tag_children(param)

            if c==[] and param_name=='index':
                params['index'] = 'DuplicatesIndexField(None)'
            elif len(c)==1:
                typename = c[0].name.title()

                if typename=='Vector':
                    partnames = sorted([p.name for p in tag_children(c[0])])
                    if partnames==['x', 'y']:
                        typename = 'X_Y'
                elif typename=='Composite':
                    partnames = sorted([p.name for p in tag_children(c[0])])
                    if partnames==['angle', 'offset', 'scale', 'skew_angle']:
                        typename = 'Transformation'

                if is_array:
                    params[param_name] = f'ParamArrayField(v.{typename})'
                else:
                    params[param_name] = f'ParamTagField(v.{typename}, XXX)'
            else:
                raise ValueError(f"{param_name} has a strange number of children: {c}")

        for left, right in params.items():
            result += f'    {left:20} = {right}\n'

    print(result)

if __name__=='__main__':
    main()
