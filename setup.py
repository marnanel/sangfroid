import os
import re
from io import open
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open('README.md', 'r', encoding='utf-8').read()

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

version = get_version('sangfroid')

setup(
    name='sangfroid',
    version=version,
    license='GPL-2',
    description='ActivityPub and Mastodon-alike social media',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Marnanel Thurman',
    author_email='marnanel@thurman.org.uk',
    packages=['sangfroid'],
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.0",
    zip_safe=False, # for now, anyway
    classifiers=[
    ],
    entry_points = {
        },
)

