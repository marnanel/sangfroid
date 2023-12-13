import gzip

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
        print("9000", magic)
        if magic not in MAGIC_SIGNATURES:
            raise ValueError(
                    f"The file {filename} isn't in a format I know how "
                    "to handle.")

        handler = MAGIC_SIGNATURES[magic]
        result = handler.__new__(handler)
        result.filename = filename
        return result

class FileContextHandler:
    def __init__(self, f):
        self.f = f

    def __enter__(self):
        return self.f

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()

class Sif(Format):
    def main_file(self):
        return FileContextHandler(open(self.filename, 'r'))

class Sifz(Format):
    def main_file(self):
        return FileContextHandler(gzip.open(self.filename, 'r'))

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
