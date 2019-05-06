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

    East Midlands,301120000,Change UK,130000,321010000
    East of England,311020000,Change UK,150000,321010000
    London,211121000,Change UK,470000,141020000
    North East,100020000,Change UK,50000,110010000
    North West,300140000,Green,150000,200240000
    Scotland,100010040,Green,30000,100100040
    South East,412111000,Change UK,80000,421111000
    South West,301110000,Liberal Democrat,10000,201111000
    Wales,200020000,Green,50000,100120000
    West Midlands,302020000,Change UK,20000,311020000
    Yorkshire and The Humber,301020000,Green,20000,300120000

Orderd by: Region, Pre-Dhondt, Recommendation, Votes, Post-Dhondt

* Free software: MIT license
* Documentation: https://eu2019model.readthedocs.io.


Features
--------

* Use input files directly from GitHub
* Drop postcode support
* Improve model!

Credits
-------

This package was created with Cookiecutter_ and the `elgertam/cookiecutter-pipenv`_ project template, based on `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`elgertam/cookiecutter-pipenv`: https://github.com/elgertam/cookiecutter-pipenv
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
