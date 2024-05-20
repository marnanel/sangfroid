import argparse
import os
import re

# synfig-core/src/synfig/paramdesc.cpp

BLEND_ENUM_RE = re.compile(r'BLEND_([A-Z_]+)=(\d+)')

DO_NOT_EDIT = (
        '#### GENERATED CODE #### DO NOT EDIT ####\n'
        f'# Produced by {os.path.basename(__file__)}\n\n'
        )

def parse_args():
    parser = argparse.ArgumentParser(
            description='convert details in Synfig sources to Python')
    parser.add_argument(
            'src', type=str,
            help='location of sources')
    args = parser.parse_args()
    return args

def write_to(filename, text):
    filename = os.path.join('sangfroid', filename)
    temp_filename = filename+'.1'

    text = DO_NOT_EDIT+text

    with open(temp_filename, 'w') as f:
        f.write(text)
    os.rename(temp_filename, filename)
    print("Written:", filename)

def main():
    args = parse_args()

    if not os.path.isdir(args.src):
        print(f"{args.src} is not a directory.")
        return

    core_dirname = os.path.join(args.src, 'synfig-core', 'src', 'synfig')

    blend_methods = {}

    with open(os.path.join(core_dirname, 'color', 'color.h'), 'r') as f:
        for line in f:
            m = BLEND_ENUM_RE.search(line)
            if m:
                name = m[1]
                val = int(m[2])

                if name in ('END', 'BY_LAYER'):
                    continue

                blend_methods[val] = name

    for i in range(len(blend_methods)):
        assert i in blend_methods

    blend_methods = [v for f,v in sorted(blend_methods.items())]

    result = ''
    result +=  'class BlendMethod(Enum):\n'

    for i,v in enumerate(blend_methods):
        result += f'    {v} = {i}\n'

    write_to(
            filename='value/blendmethod.py',
            text=result,
            )

if __name__=='__main__':
    main()
