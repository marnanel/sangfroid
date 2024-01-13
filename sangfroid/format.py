import gzip
import bs4

class Format:
    """
    A disk file, containing an animation saved in a particular format.

    It also allows access to files dependent on the main file.

    Fields:
        filename (str): the filename.
    """

    def __init__(self):
        raise NotImplementedError(
                "Create formats using from_filename().")

    def main_file(self):
        """
        Returns the main canvas file.

        Returns:
            file context handler
        """
        
        raise NotImplementedError()

    def __getitem__(self, v):
        """
        Looks up a file referred to by the main file.
        """
        raise NotImplementedError()

    @classmethod
    def from_filename(cls, filename):
        """
        Given a filename, returns a Format of the appropriate subclass,
        initialised with the filename.

        Args:
            filename (str): the filename

        Returns:
            Format

        Raises:
            ValueError: if the filename isn't in a format we know
                how to handle.
        """
        with open(filename, 'rb') as f:
            magic = f.read(2)
        if magic not in MAGIC_SIGNATURES:
            raise ValueError(
                    f"The file {filename} isn't in a format I know how "
                    "to handle.")

        handler = MAGIC_SIGNATURES[magic]
        result = handler.__new__(handler)
        result.filename = filename
        return result

    def save(self, content, filename=None):
        """
        Saves a file to disk.

        Args:
            content (bs4.Document): the XML document to save
            filename (str or None): the filename to save under;
                if None, we use self.filename; if not None,
                this is a "save as", so self.filename will
                be set to this value.
        """
        raise NotImplementedError()

    def _filename_for_saving(self, filename):
        if filename is None:
            filename = self.filename
        else:
            self.filename = filename

        return filename

    def _write_to_file(self, f, content):
        f.write(content.encode(formatter=_SifFormatter(), indent_level=9))

class FileContextHandler:
    def __init__(self, f):
        self.f = f

    def __enter__(self):
        return self.f

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()

class _SifFormatter(bs4.formatter.XMLFormatter):
    def __init__(self, *args, **kwargs):
        kwargs['indent'] = 2
        super().__init__(*args, **kwargs)

class Sif(Format):
    def main_file(self):
        return FileContextHandler(open(self.filename, 'r'))

    def save(self, content, filename=None):
        filename = self._filename_for_saving(filename)

        with open(filename, 'wb') as f:
            self._write_to_file(f, content)

class Sifz(Format):
    def main_file(self):
        return FileContextHandler(gzip.open(self.filename, 'r'))

    def save(self, content, filename=None):
        filename = self._filename_for_saving(filename)

        with gzip.open(filename, 'wb') as f:
            self._write_to_file(f, content)

class Sfg(Format):
    def main_file(self):
        raise ValueError(
                '.sfg is not yet supported. See: \n'
                'https://gitlab.com/marnanel/sangfroid/-/issues/2'
                )

MAGIC_SIGNATURES = {
        b'<?':       Sif,        # start of XML doctype
        b'\x1f\x8b': Sifz,       # gzip header
        b'PK':       Sfg,        # zipfile header (RIP Phil Katz)
        }
