# -*- coding: utf-8 -*-
"""
Provides DotAccessDict class which makes accessing dict items by dot notation.

DotAccessDict class can handle nested dictionaries with arbitray number of
dicts and lists nested inside each other.

Similar works:
 - https://github.com/mewwts/addict
 - https://github.com/makinacorpus/easydict
 - https://github.com/drgrib/dotmap
"""


__author__ = 'Reza Behzadan'
__email__ = 'rbehzadan@gmail.com'
__copyright__ = 'Copyright © 2017 Reza Behzadan'
__date__ = '2017-01-16'
__modified__ = '2017-04-17'

__license__ = 'MIT'
__version__ = '0.0.1'
__status__ = 'development'


import re


data = """
{
  "families": {
    "members": [
      ["Ricardo", "Alexis", "Victor"],
      [["Shanaya", "Sherry"], "Mary", "Mateo", "Zoe"]
    ],
    "family1": "O'Barian",
    "family2": "Solloway"
  },
  "proxies": [
    {"http": "192.168.0.1:8080", "https": "192.168.0.1:8081"},
    {"http": "192.168.1.1:8080", "https": "192.168.1.1:8081"},
    [
      "192.168.2.1", "192.168.3.1", "192.168.4.1",
      "192.168.5.1", "192.168.6.1", "192.168.7.1"
    ]
  ],
  "databases": {
    "mongodb": {
      "url": "mongodb://localhost:27017",
      "host": "localhost",
      "port": 27017,
      "username": "user",
      "password": "pass"
    },
    "redis": {
      "url": "redis://localhost"
    }
  }
}
"""
import json
data = json.loads(data)


def _enumerate(obj):
    """enumerate lists (with indexes) and dicts (with keys)
    """
    if isinstance(obj, (set, tuple, list)):
        for i, v in enumerate(obj):
            yield i, v
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield k, v
    # else:
        # return

def _flatten_helper(obj, path=''):
    myself = _flatten_helper
    items = []
    for k, v in _enumerate(obj):
        if isinstance(k, int):
            k = '[%s]' % k
            new_path = path + k if path else k
        else:
            # TODO: could we use k=str(k) and replace whitespaces with _?
            if not isinstance(k, str):
                raise TypeError('Need ``str`` you gave ``%s``' % type(k))
            new_path = path + '.' + k if path else k
        if isinstance(v, (set, tuple, list, dict)):
            items.extend(myself(v, new_path))
        else:
            items.append((new_path, v))
    return items

def _flatten(d):
    """Return dict of flatten nested dict
    """
    if not isinstance(d, dict):
        raise TypeError('Need dict-like object')
    return dict(_flatten_helper(d))


class DotAccessDict(dict):
    _index_pat = re.compile('\[(\-?\d+?)\]')
    _valid_key_pat = re.compile(
            '^([A-Za-z_]+\d*(\[\-?\d+?\])*)(\.[A-Za-z_]+\d*(\[\-?\d+?\])*)*$')

    def __init__(self, d=None):
        super().__init__()
        if d is not None:
            if not isinstance(d, dict):
                raise TypeError('Need dict like object.')
            self._parse(d)

    @classmethod
    def _parse_list_like_object(cls, lst_obj):
        items = []
        for i in lst_obj:
            if isinstance(i, (set, tuple, list)):
                v = cls._parse_list_like_object(i)
            elif isinstance(i, cls):
                v = i
            elif isinstance(i, dict):
                v = cls(i)
            else:
                v = i
            items.append(v)
        return items

    def _parse(self, d):
        cls = self.__class__
        for k, v in d.items():
            if isinstance(v, cls):
                self[k] = v
            elif isinstance(v, dict):
                self[k] = cls(v)
            elif isinstance(v, (set, tuple, list)):
                self[k] = cls._parse_list_like_object(v)
            else:
                self[k] = v

    def update(self, other):
        cls = self.__class__
        if not isinstance(other, (cls, dict)):
            raise TypeError('Need dict like object.')
        for k in other:
            if k not in self:
                self[k] = other[k]
            elif isinstance(self[k], cls) and \
                 isinstance(other[k], (cls, dict)):
                self[k].update(other[k])
            else:
                self[k] = other[k]

    def get(self, key, d=None):
        cls = self.__class__
        if not cls._valid_key_pat.match(key):
            raise SyntaxError('Invalid key')
        parts = key.split('.')
        head = parts[0]
        tail = '.'.join(parts[1:])
        indexes = map(int, cls._index_pat.findall(head))
        head = head.split('[')[0]
        v = super().get(head, d)
        for index in indexes:
            try:
                v = v[index]
            except (TypeError, IndexError):
                return d
        if tail:
            if not isinstance(v, cls):
                return d
            return v.get(tail, d)
        return v

    def set(self, key, value):
        cls = self.__class__
        if not cls._valid_key_pat.match(key):
            raise SyntaxError('Invalid key')
        if isinstance(value, str):
            exec('self.%s="%s"' % (key, value))
        else:
            exec('self.%s=%s' % (key, value))

    def flatten(self):
        return _flatten(self)

    @classmethod
    def _to_dict_helper(cls, lst):
        l = []
        for item in lst:
            if isinstance(item, cls):
                l.append(item.to_dict())
            elif isinstance(item, list):
                l.append(cls._to_dict_helper(item))
            else:
                l.append(item)
        return l

    def to_dict(self):
        cls = self.__class__
        d = {}
        for k, v in self.items():
            if isinstance(v, cls):
                d[k] = v.to_dict()
            elif isinstance(v, list):
                d[k] = cls._to_dict_helper(v)
            else:
                d[k] = v
        return d

    def __setattr__(self, key, value):
        cls = self.__class__
        if isinstance(value, dict) and not isinstance(value, cls):
            self[key] = cls(value)
        elif isinstance(value, (list, tuple, set)):
            self[key] = cls._parse_list_like_object(value)
        else:
            self[key] = value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def __getattr__(self, key):
        cls = self.__class__
        if key not in self:
            m = cls()
            self[key] = m
            return m
        return super().__getitem__(key)

    def __dir__(self):
        return super().keys()

