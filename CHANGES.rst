===================
 changes for alnvu
===================

0.3.3
=====

* fix ``--sort-by-name FILE`` (where FILE contains original names if
  ``--rename -from-file`` is also used.
* remove trailing whitespace from terminal output

0.3.2
=====

* fix --rename-from-file [GH7]

0.3.1
=====

* python3 support
* add dependency on ``fastalite``
* remove ``colorbrewer`` from setup.py and hide --annotation-file option
  when ``colorbrewer`` is not installed
* add tests, and configure automated testing on Travis CI

0.2.1
=====

* add CHANGES.rst (better late than never!)
* add option -R/--trim-to

