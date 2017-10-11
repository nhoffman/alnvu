import os
import subprocess
from setuptools import setup

subprocess.call(
    ('mkdir -p {pkg}/data && '
     'git describe --tags --dirty > {pkg}/data/ver.tmp '
     '&& mv {pkg}/data/ver.tmp {pkg}/data/ver '
     '|| rm -f {pkg}/data/ver.tmp').format(pkg='alnvu'),
    shell=True, stderr=open(os.devnull, "w"))

# import must follow 'git describe' command above to update version
from alnvu import __version__

params = {'author': 'Noah Hoffman',
          'author_email': 'noah.hoffman@gmail.com',
          'description': ('Reformat and condense multiple sequence alignments '
                          'to highlight variability'),
          'name': 'alnvu',
          'package_dir': {'alnvu': 'alnvu'},
          'packages': ['alnvu'],
          'package_data': {'alnvu': ['data/*']},
          'scripts': ['av'],
          'url': 'http://github.com/nhoffman/alnvu',
          'version': __version__,
          'requires': ['python (>= 2.7)'],
          'install_requires': [
              'Jinja2>=2.7',
              'colorbrewer>=0.1.1',
              'reportlab>=3.0'
              ],
      }

setup(**params)
