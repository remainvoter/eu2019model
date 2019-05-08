===========
eu2019model
===========


.. image:: https://img.shields.io/pypi/v/eu2019model.svg
        :target: https://pypi.python.org/pypi/eu2019model

.. image:: https://img.shields.io/travis/DrNickMartin/eu2019model.svg
        :target: https://travis-ci.org/DrNickMartin/eu2019model

.. image:: https://readthedocs.org/projects/eu2019model/badge/?version=latest
        :target: https://eu2019model.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Model to be used as a recommendation engine for people wishing to vote remain in the EU 2019 elections in the UK

The current model output looks like this:

.. code-block::

    East Midlands,301120000,Change UK,123500,321010000
    East of England,311020000,Change UK,142000,321010000
    North East,100020000,Change UK,49000,110010000
    North West,300140000,Green,146500,200240000
    Scotland,100010040,Green,27000,100100040
    South East,412111000,Change UK,70500,421111000
    South West,301110000,Liberal Democrat,500,201111000
    Wales,200020000,SNP/Plaid Cymru,11000,100020010
    West Midlands,302020000,Change UK,14000,311020000
    Yorkshire and The Humber,301020000,Green,13000,300120000

Orderd by: Region, Pre-Dhondt, Recommendation, Votes, Post-Dhondt

* Free software: MIT license
* Documentation: https://eu2019model.readthedocs.io.


To Do
--------

* Use input files directly from GitHub
* Drop postcode support
* Fix travis-CI
* Dploy to PyPi
* Improve model!

Credits
-------

This package was created with Cookiecutter_ and the `elgertam/cookiecutter-pipenv`_ project template, based on `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`elgertam/cookiecutter-pipenv`: https://github.com/elgertam/cookiecutter-pipenv
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
