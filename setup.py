import os
from setuptools import setup

from alnvu import __version__

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()


params = {
    'author': 'Noah Hoffman',
    'author_email': 'noah.hoffman@gmail.com',
    'description': ('Reformat and condense multiple sequence alignments '
                    'to highlight variability'),
    'long_description': long_description,
    'name': 'alnvu',
    'package_dir': {'alnvu': 'alnvu'},
    'packages': ['alnvu'],
    'package_data': {'alnvu': ['data/*']},
    'url': 'http://github.com/nhoffman/alnvu',
    'version': __version__,
    'requires': ['python (>= 2.7)'],
    'install_requires': [
        'Jinja2>=2.7',
        'reportlab>=3.0',
        'fastalite>=0.3',
    ],
    'entry_points': {
        'console_scripts': ['av = alnvu.av:main']
    },
    'test_suite': 'tests',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
}

setup(**params)
