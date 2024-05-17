# Finds symbols from sangfroid/layer/*.py, for the use of pick-and-mix-to-layers.py
import json
import glob
import re

OUTPUT_FILENAME = 'layer-details.json'

LAYER_CLASS_DEF_RE = re.compile(r"""class ([A-Za-z0-9_]+)\(([A-Za-z0-9_]+)""")
SYMBOL_RE = re.compile(r"""SYMBOL *= *['"]([^'"]*)""")

results = {}

current_classname = None

for thing in glob.glob('sangfroid/layer/*.py'):
    with open(thing, 'r') as f:
        print("Reading:", thing)
        for line in f.readlines():
            m = LAYER_CLASS_DEF_RE.search(line)
            if m is not None:
                classname, superclassname = m.groups()
                if superclassname!='Layer':
                    continue
                current_classname = classname

                assert classname not in results

                results[current_classname] = {}

            if current_classname in results:
                sm = SYMBOL_RE.search(line)
                if sm is not None:
                    results[current_classname]['symbol'] = sm.groups()[0]

with open(OUTPUT_FILENAME, 'w') as f:
    json.dump(results, f, indent=4,
              sort_keys=True,
              ensure_ascii = False,
              )

print("Written:", OUTPUT_FILENAME)
