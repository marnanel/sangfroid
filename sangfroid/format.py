import gzip
import os
from bs4 import BeautifulSoup

class Format:
    """
    A disk file, containing an animation saved in a particular format.

    It also allows access to files dependent on the main file.

    Fields:
        filename (str): the filename.

    Class fields:
        extensions (tuple of str): the filename extensions which
            can be used for this format, without leading dots.
        magic_number (bytes): the first two characters of
            files of this format.
    """

    def __init__(self):
        raise NotImplementedError(
                "Create formats using from_filename().")

    def main_file(self):
        """
        Returns the parsed XML of the main document.

        For the filename, see the `filename` field.

        Returns:
            BeautifulSoup.Tag
        """
        raise NotImplementedError()

    def __getitem__(self, v):
        """
        Looks up a file referred to by the main file.
        """
        return self._subfiles[v]

    def __len__(self):
        """
        Returns the number of files referred to in the main file.

        Returns:
            int
        """
        return len(self._subfiles)

    def items(self):
        return self._subfiles.items()

    def keys(self):
        return self._subfiles.keys()

    def values(self):
        return self._subfiles.values()

    @classmethod
    def from_filename(cls, filename,
                      load = True,
                      ):
        """
        Given a filename, returns a Format of the appropriate subclass,
        possibly loaded from the file of that name.

        Args:
            filename (str): the filename
            load (bool): if True, load the file with that name

        Returns:
            Format

        Raises:
            ValueError: if the filename isn't in a format we know
                how to handle.
            FileNotFoundError: if load==True and the file doesn't
                exist.
        """
        assert filename is not None

        if load:
            with open(filename, 'rb') as f:
                magic = f.read(2)

            if not magic:
                raise ValueError("The file {filename} is empty.")

            handlers = [h for h in cls.handlers()
                        if h.magic_number==magic]
            if not handlers:
                raise ValueError(
                        f"The file {filename} isn't in a format I know how "
                        "to handle.")
        else:
            extension = os.path.splitext(filename)[1].lower()
            if extension.startswith('.'):
                extension = extension[1:]

            handlers = [h for h in cls.handlers()
                        if extension in h.extensions]
            if not handlers:
                raise ValueError(
                        "I don't know how to handle files with the "
                        f"extension {extension}."
                        )

        assert len(handlers)==1

        handler = handlers[0]

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
        f.write(str(content).encode('UTF-8'))

    @classmethod
    def handlers(cls):
        """
        Returns all known subclasses of Format.
        """
        return [
                h for h in globals().values()
                if isinstance(h, type)
                and issubclass(h, Format)
                and h!=Format
                ]

class FileContextHandler:
    def __init__(self, f):
        self.soup = BeautifulSoup(
                f,
                features = 'xml',
                )

    def __enter__(self):
        return self.soup

    def __exit__(self, exc_type, exc_value, traceback):
        pass

class Sif(Format):

    magic_number = b'<?' # start of XML doctype
    extensions = ('sif',)

    def main_file(self):
        return FileContextHandler(open(self.filename, 'r'))

    def save(self, content, filename=None):
        filename = self._filename_for_saving(filename)

        with open(filename, 'wb') as f:
            self._write_to_file(f, content)

class Sifz(Format):

    magic_number = b'\x1f\x8b' # gzip header
    extensions = ('sifz',)

    def main_file(self):
        return FileContextHandler(gzip.open(self.filename, 'r'))

    def save(self, content, filename=None):
        filename = self._filename_for_saving(filename)

        with gzip.open(filename, 'wb') as f:
            self._write_to_file(f, content)

class Sfg(Format):
    
    magic_number = b'PK' # zipfile header (RIP Phil Katz)
    extensions = ('sfg',)

    def main_file(self):
        raise ValueError(
                '.sfg is not yet supported. See: \n'
                'https://gitlab.com/marnanel/sangfroid/-/issues/2'
                )
