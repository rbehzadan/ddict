# -*- coding: utf-8 -*-
"""
Provides DotAccessDict class which makes accessing dict items by dot notation.

DotAccessDict class can handle nested dictionaries with arbitray number of
dicts and lists nested inside each other.

Notes:
  - As nested elements can be constructed with dot notation, the return value
    of non existing attribute/key is DotAccessDict
  - All key/attributes that are not int or str, will be converted to str
  - Multiple arguments in constructor, update the values of existing keys and
    not replace them.
  - 



TODO:
  - PEP 363 -- Syntax For Dynamic Attribute Access

Similar works:
 - https://github.com/mewwts/addict
 - https://github.com/makinacorpus/easydict
 - https://github.com/drgrib/dotmap
"""


__author__ = 'Reza Behzadan'
__email__ = 'rbehzadan@gmail.com'
__copyright__ = 'Copyright © 2017 Reza Behzadan'
__date__ = '2017-01-16'
__modified__ = '2017-04-19'

__license__ = 'MIT'
__version__ = '0.0.4'
__status__ = 'development'


import re


def isiterable(obj):
    """Return True if ``obj`` is not str, and is iterable
    """
    return hasattr(obj, '__iter__') and not isinstance(obj, str)

def _enumerate(obj):
    """enumerate lists (with indexes) and dicts (with keys)
    """
    if isinstance(obj, (set, tuple, list)):
        for i, v in enumerate(obj):
            yield i, v
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield k, v

def flatten(d, max_depth=10):
    """Return dict of flatten nested dict
    """
    if not isinstance(d, dict):
        raise TypeError('Need dict-like object')
    def _flatten_helper(obj, path=''):
        nonlocal max_depth
        myself = _flatten_helper
        items = []
        for k, v in _enumerate(obj):
            # note: k's (keys) are either int or str and nothing else
            if isinstance(k, int):
                k = '[%s]' % k
                new_path = path + k if path else k
            else:
                new_path = path + '.' + k if path else k
                if new_path.count('.') >= max_depth:
                    continue
            if isinstance(v, (set, tuple, list, dict)):
                items.extend(myself(v, new_path))
            else:
                items.append((new_path, v))
        return items
    # print("---------> depth=%s"%depth)
    return dict(_flatten_helper(d))


class DotAccessDict(dict):
    _index_pat = re.compile('\[(\-?\d+?)\]')
    _valid_attr = re.compile('^[_a-zA-Z]+[_a-zA-Z0-9]*$')
    _valid_key_pat = re.compile(
            '^([A-Za-z_]+\d*(\[\-?\d+?\])*)(\.[A-Za-z_]+\d*(\[\-?\d+?\])*)*$')

    def __init__(self, *args, **kwargs):
        cls = self.__class__
        super().__init__()
        for arg in args:
            if not isiterable(arg):
                raise TypeError('Need collection')
            if isinstance(arg, dict):
                self.update(arg)
            # elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
            elif isinstance(arg, tuple):
                self[arg[0]] = arg[1]
            else:
                for key, val in iter(arg):
                    self[key] = val
        for key, val in kwargs.items():
            self[key] = val

    @classmethod
    def __parse_list_like_object(cls, lst_obj):
        items = []
        for i in lst_obj:
            if isinstance(i, (set, tuple, list)):
                v = cls.__parse_list_like_object(i)
            elif isinstance(i, cls):
                v = i
            elif isinstance(i, dict):
                v = cls(i)
            else:
                v = i
            items.append(v)
        return items

    def update(self, other):
        cls = self.__class__
        if not isinstance(other, dict):
            raise TypeError('Need dict like object.')
        for k, v in other.items():
            if k not in self:
                self[k] = v
            elif isinstance(self[k], cls) and isinstance(v, dict):
                self[k].update(v)
            else:
                self[k] = v

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
        return flatten(self)

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

    def __set(self, key, value):
        cls = self.__class__
        if not isinstance(key, (str, int)):
            key = str(key)
        if isinstance(value, dict) and not isinstance(value, cls):
            val = cls(value)
        elif isinstance(value, (list, tuple, set)):
            val = cls.__parse_list_like_object(value)
        else:
            val = value
        super().__setitem__(key, val)

    def __setattr__(self, key, value):
        self.__set(key, value)

    def __setitem__(self, key, value):
        self.__set(key, value)

    def __getattr__(self, key):
        cls = self.__class__
        if key not in self:
            m = cls()
            self[key] = m
            return m
        return super().__getitem__(key)

    def __dir__(self):
        return super().keys()

