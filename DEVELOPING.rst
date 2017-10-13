==================
 developing alnvu
==================

tests
=====

Run tests with::

  python setup.py test

PyPi
====

Release versions should be identified by git tags::

  git tag -a -m 'first release on pipy' 0.1.0

If you have not done so create a ~/.pypirc file containing your PyPI
credentials::

  python setup.py register

Build and upload (requires `twine` and `wheel` packages)::

  rm -rf dist build
  python setup.py clean
  python setup.py sdist bdist_wheel
  twine upload dist/*

