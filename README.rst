|Build Status| |Coverage Status|

=============
DotAccessDict
=============

DotAccessDict class can handle nested dictionaries with arbitray number
of dicts and lists, nested inside each other.

Usage:
~~~~~~

.. code:: python

    >>> from ddict import DotAccessDict
    >>> d = DotAccessDict()
    >>> d
    {}
    >>> d.person
    {}
    >>> d.person.name = 'Jack'
    >>> d
    {'person': {'name': 'Jack'}}
    >>> d['person']['name']
    'Jack'
    >>> d['person'].name
    'Jack'
    >>> d.person['name']
    'Jack'
    >>> joe = dict(name='Joe', age=18)
    >>> d.person.brothers = [joe, 'John', 'Pat']
    >>> d.person.brothers[0].age
    18
    >>> d.get('person.brothers[1]')
    'John'
    >>> d.set('person.brothers[2]', 'James')
    >>> d.person.brothers[2]
    'James'
    >>> d.flatten()
    {'person.brothers[0].age': 18,
     'person.brothers[0].name': 'Joe',
     'person.brothers[1]': 'John',
     'person.brothers[2]': 'James',
     'person.name': 'Jack'}

Similar works:
~~~~~~~~~~~~~~

-  https://github.com/mewwts/addict
-  https://github.com/makinacorpus/easydict
-  https://github.com/drgrib/dotmap

.. |Build Status| image:: https://travis-ci.org/rbehzadan/ddict.svg?branch=master
   :target: https://travis-ci.org/rbehzadan/ddict
.. |Coverage Status| image:: https://coveralls.io/repos/github/rbehzadan/ddict/badge.svg
   :target: https://coveralls.io/github/rbehzadan/ddict
