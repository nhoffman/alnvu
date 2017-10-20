import traceback
import subprocess
import os
import sys


def get_version(datadir=None):
    """When executed from setup.py, creates the file "{datadir}/ver"
    containing a version number corresponding to the output of 'git
    describe --tags --dirty'. In all cases, the contents of this file
    is converted into a (hopefully) PEP-440 compliant version string
    and returned. ``datadir`` is an optional path to package data;
    when not provided, assumes package data resides in a directory
    named "data" in the same directory as this file (which in turn is
    expected to be placed in the same directory as the top-level
    package __init__.py). Further notes and assumptions:

    - get_version() should be called from the package __init__.py, for example:
        from ._version import get_version
        __version__ = get_version()
    - at least one git tag is defined
    - setup.py should import
    - setuptools.setup includes a directive to include {datadir}/ver in a
      package distribution, for example
      ``setuptools.setup(package_data={'my_package': ['data/*']})``

    """

    datadir = datadir or os.path.join(os.path.dirname(__file__), 'data')
    version_file = os.path.join(datadir, 'ver')

    # only try to create the version file if setup.py is someplace in the stack
    stack = traceback.extract_stack()
    try:
        in_setup = any(s.filename.endswith('setup.py') for s in stack)
    except AttributeError:
        in_setup = any(s[0].endswith('setup.py') for s in stack)

    if in_setup:
        sys.stdout.write('updating {} with version '.format(version_file))
        subprocess.call(
            ('mkdir -p {datadir} && '
             'git describe --tags --dirty > {file}.tmp '
             '&& mv {file}.tmp {file} '
             '|| rm -f {file}.tmp').format(datadir=datadir, file=version_file),
            shell=True, stderr=open(os.devnull, "w"))

    try:
        with open(version_file) as f:
            version = f.read().strip().replace('-', '+', 1).replace('-', '.')
    except Exception:
        version = ''

    if in_setup:
        sys.stdout.write(version + '\n')

    return version
