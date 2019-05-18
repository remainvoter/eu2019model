===========
eu2019model
===========


.. image:: https://img.shields.io/pypi/v/eu2019model.svg
        :target: https://pypi.python.org/pypi/eu2019model

.. image:: https://travis-ci.org/remainvoter/eu2019model.svg?branch=master
        :target: https://travis-ci.org/remainvoter/eu2019model

.. image:: https://readthedocs.org/projects/eu2019model/badge/?version=latest
        :target: https://eu2019model.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



Model to be used as a recommendation engine for people wishing to vote
remain in the EU 2019 elections in the UK

The current model output looks like this:

.. code-block::

        East Midlands,301021000,Liberal Democrat,210000,301012000
        East of England,311011000,Change UK,200000,221011000
        London,100133000,Liberal Democrat,500000,100025000
        North East,200010000,Liberal Democrat,50000,100011000
        North West,200051000,Green,70000,200141000
        Scotland,101011020,SNP/Plaid Cymru,20000,100011030
        South East,312112000,Change UK,740000,242011000
        South West,300012000,Liberal Democrat,260000,300003000
        Wales,200020000,SNP/Plaid Cymru,60000,100020010
        West Midlands,300130000,Change UK,90000,210130000
        Yorkshire and The Humber,301020000,Liberal Democrat,50000,300021000

Orderd by: Region, Pre-Dhondt, Recommendation, Votes, Post-Dhondt

* Free software: MIT license
* Documentation: https://eu2019model.readthedocs.io.

Running
--------
Until the package is made availible on PyPi, it can be run
by completing the following:

1. Clone the repo using git:

.. code-block::

        git clone https://github.com/remainvoter/eu2019model.git

2. cd into the folder and install a local environment with :code:`pipenv`

.. code-block::

        cd eu2019model
        pip install pipenv
        pipenv install

3. run the module from within the environment:

.. code-block::

        pipenv run python -m recommend.remainvoter -h

To Do
--------

* Fix travis-CI
* Dploy to PyPi

Credits
-------

This package was created with Cookiecutter_ and the 
`elgertam/cookiecutter-pipenv`_ project template, based on 
`audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`elgertam/cookiecutter-pipenv`: https://github.com/elgertam/cookiecutter-pipenv
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
