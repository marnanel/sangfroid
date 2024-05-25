import os
import glob
import re

CLASSNAME_RE = re.compile(r'^class ([A-Za-z0-9_]+)')
START_BLOCK_RE = re.compile(r'^( *)### {{{ *([A-Za-z0-9_]*)')
END_BLOCK_RE = re.compile(r'^ *### }}}')

class Replacer:
    def __init__(self,
                 fields = None,
                 verbose = False,
                 ):
        self.fields = fields or {}
        self.verbose = verbose
        self.seen_fields = set()

    def add(self, blockname, value):
        self.fields[blockname] = value

    def handle_all_files(self):

        if not self.fields:
            return

        for filename in glob.glob('sangfroid/**/*.py',
                                  recursive=True,
                                  ):
            self.handle(filename)

    def handle(self, filename):

        if not self.fields:
            return

        result = ''

        latest_class_name = None
        current_block_name = None
        current_indent = None
        changed = False
        ignore = False

        with open(filename, 'r') as f:

            for i, line in enumerate(f):
                if self.verbose:
                    print("%4d %30s %s" % (
                        i,
                        current_block_name or '',
                        line.rstrip(),
                        ))
                m = CLASSNAME_RE.search(line)
                if m:
                    latest_class_name = m.groups()[0]

                m = START_BLOCK_RE.search(line)
                if m:
                    current_indent = len(m.groups()[0])
                    current_block_name = m.groups()[1]
                    if current_block_name == '':
                        current_block_name = latest_class_name
                        latest_class_name = None

                    if not current_block_name:
                        raise ValueError(f"{filename}:{i}: beginning block with no name")

                    result += line
                    self.seen_fields.add(current_block_name)

                    if current_block_name not in self.fields:
                        ignore = False

                    else:
                        indent_s = ' '*current_indent
                        next_lines = [
                                (indent_s+line).rstrip()
                                for line in
                                self.fields[current_block_name].split('\n')
                                ]
                        result += '\n'.join(next_lines)
                        ignore = True
                        changed = True
                    continue

                m = END_BLOCK_RE.search(line)
                if m:
                    if current_block_name is None:
                        raise ValueError(f"{filename}:{i}: ended block without starting one")
                    result += '\n'
                    line = (' '*current_indent) + line.strip() + '\n'
                    current_block_name = None
                    current_indent = None
                    ignore = False

                if not ignore:
                    result += line

            if current_block_name is not None:
                raise ValueError(f"{filename}:{i}: file ended in the middle of a block")

            if changed:
                self.write_to(filename, result)

    def check_everything_was_seen(self):
        for name in sorted(self.fields.keys()):
            if name not in self.seen_fields:
                print(f"{name}: specified, but no blocks were found with that name")

    @classmethod
    def write_to(cls, filename, text):
        temp_filename = filename+'.1'

        with open(temp_filename, 'w') as f:
            f.write(text)
        os.rename(temp_filename, filename)
        print("Written:", filename)

if __name__=='__main__':
    r = Replacer(
            {'foo': 'bar'},
            )
    r.handle_all_files()
    r.check_everything_was_seen()
