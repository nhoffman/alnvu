from distutils.core import setup

from alnvu.__init__ import __version__

params = {'author': 'Noah Hoffman',
          'author_email': 'noah.hoffman@gmail.com',
          'description': 'Reformat and condense multiple sequence alignments to highlight variability',
          'name': 'alnvu',
          'package_dir': {'alnvu': 'alnvu'},
          'packages': ['alnvu'],
          'scripts': ['av'],
          'url': 'http://github.com/nhoffman/alnvu',
          'version': __version__,
          'requires':['python (>= 2.7)']}

setup(**params)
