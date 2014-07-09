==================
 developing alnvu
==================

PyPi
====

Make sure to update the __version__ variable in the bioscons/__init__.py file.

If you have not done so create a ~/.pypirc file containing your PyPI
credentials::

  python setup.py register

Build and upload (requires `twine` and `wheel` packages)::

  python setup.py clean
  python setup.py sdist bdist_wheel
  twine upload dist/*



