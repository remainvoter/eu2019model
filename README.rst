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
        pipenv install --dev

3. run the module from within the environment:

.. code-block::

        pipenv run python -m eu2019model.recommend --update --defence

Authors
-------

This model was developed by the Remain Voter group, an independent group of volunteers who wanted to provide helpful, data driven recommendations for those unsure which remain party to vote for in the EU elections. Full details of the implementation method and assumptions made in the model can be found on the Remain Voter website: https://www.remainvoter.com.

Lead model designer: Cheryl Hung
Principal developer: Nick Martin

Credits
-------

This package was created with Cookiecutter_ and the 
`elgertam/cookiecutter-pipenv`_ project template, based on 
`audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`elgertam/cookiecutter-pipenv`: https://github.com/elgertam/cookiecutter-pipenv
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
