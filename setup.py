from setuptools import setup
import subprocess

from alnvu.__init__ import __version__

subprocess.call('git log --pretty=format:%h -n 1 > alnvu/data/sha', shell = True)
subprocess.call('git shortlog --format="XXYYXX%h" | grep -c XXYYXX > alnvu/data/ver', shell = True)

params = {'author': 'Noah Hoffman',
          'author_email': 'noah.hoffman@gmail.com',
          'description': 'Reformat and condense multiple sequence alignments to highlight variability',
          'name': 'alnvu',
          'package_dir': {'alnvu': 'alnvu'},
          'packages': ['alnvu'],
          'scripts': ['av'],
          'url': 'http://github.com/nhoffman/alnvu',
          'version': __version__,
          'requires':['python (>= 2.7)'],
          'install_requires': [
              'Jinja2>=2.7',
              'colorbrewer>=0.1.1',
              'reportlab>=3.0'
              ]
      }

setup(**params)
