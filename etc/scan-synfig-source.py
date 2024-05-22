import argparse
import os
import re
from sangfroid.template.replacer import Replacer

BLEND_ENUM_RE = re.compile(r'BLEND_([A-Z_]+)=(\d+)')

def parse_args():
    parser = argparse.ArgumentParser(
            description='convert details in Synfig sources to Python')
    parser.add_argument(
            'src', type=str,
            help='location of sources')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    if not os.path.isdir(args.src):
        print(f"{args.src} is not a directory.")
        return

    core_dirname = os.path.join(args.src, 'synfig-core', 'src', 'synfig')

    blend_methods = {}
    replacer = Replacer()

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

    result = '\n'

    for i,v in enumerate(blend_methods):
        result += f'{v} = {i}\n'

    replacer.add('BlendMethod', result)
    replacer.handle_all_files()
    replacer.check_everything_was_seen()

if __name__=='__main__':
    main()
