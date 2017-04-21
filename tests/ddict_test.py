import json
import pytest

import ddict
import ddict.ddict

enum = ddict.ddict._enumerate
flatten = ddict.ddict.flatten

from ddict import DotAccessDict
Dict = ddict.DotAccessDict
type_ddict = type(Dict)

print('\n*** Testing ddict version %s ***' % ddict.ddict.__version__)

joe = dict(name='Joe', age=18, sex='M')
jill = dict(name='Jill', age=22, sex='F')
jack = dict(name='Jack', age=8, sex='M')
jane = dict(name='Jane', age=14, sex='F')
john = dict(name='John', age=55, sex='M')
mary = dict(name='Mary', age=50, sex='F')
pitt = dict(name='Pitt', age=60, sex='M')
rose = dict(name='Rose', age=58, sex='F')

john['children'] = [[joe, jack], [jill, jane]]
joe['brother'] = jack
joe['sisters'] = [jill, jane]
john_flat = '{"name": "John", "age": 55, "sex": "M", "children[0][0].name": "Joe", "children[0][0].age": 18, "children[0][0].sex": "M", "children[0][0].brother.name": "Jack", "children[0][0].brother.age": 8, "children[0][0].brother.sex": "M", "children[0][0].sisters[0].name": "Jill", "children[0][0].sisters[0].age": 22, "children[0][0].sisters[0].sex": "F", "children[0][0].sisters[1].name": "Jane", "children[0][0].sisters[1].age": 14, "children[0][0].sisters[1].sex": "F", "children[0][1].name": "Jack", "children[0][1].age": 8, "children[0][1].sex": "M", "children[1][0].name": "Jill", "children[1][0].age": 22, "children[1][0].sex": "F", "children[1][1].name": "Jane", "children[1][1].age": 14, "children[1][1].sex": "F"}'
john_flat = json.loads(john_flat)
john_flat1 = '{"name": "John", "age": 55, "sex": "M"}'
john_flat1 = json.loads(john_flat1)
john_flat2 = '{"name": "John", "age": 55, "sex": "M", "children[0][0].name": "Joe", "children[0][0].age": 18, "children[0][0].sex": "M", "children[0][1].name": "Jack", "children[0][1].age": 8, "children[0][1].sex": "M", "children[1][0].name": "Jill", "children[1][0].age": 22, "children[1][0].sex": "F", "children[1][1].name": "Jane", "children[1][1].age": 14, "children[1][1].sex": "F"}'
john_flat2 = json.loads(john_flat2)

# jack['brother'] = joe
# jack['sisters'] = [jill, jane]
# jill['brothers'] = [joe, jack]
# jill['sister'] = jane
# jane['brothers'] = [joe, jack]
# jane['sister'] = jill



siblings = [[joe, jill, jack, jane], [pitt, john]]
brothers = [[joe, jack], [pitt, john]]
sisters = [jane, jill]

n1 = dict(name='A', rank=1)
n2 = dict(name='B', rank=2)
n3 = dict(name='C', rank=3)
n4 = dict(name='D', rank=4)
n5 = dict(name='E', rank=5)
n6 = dict(name='F', rank=6)
n7 = dict(name='G', rank=7)
n8 = dict(name='H', rank=8)
n9 = dict(name='I', rank=9)
n1['n'] = [n2, n3]
n2['n'] = [n4, n5, n6]
n3['n'] = [n7, n8]
n5['n'] = [n9]

jack2 = {
  'name': 'Jack',
  'age': 59,
  'children': [
      ['Bob', 'Charly', 'Alen'],
      ['Alice', 'Ruby']]
}

def test__enumerate_bad_args():
    assert list(enum(12)) == []
    assert list(enum('jack')) == []
    assert list(enum(12.25)) == []
    assert list(enum(None)) == []
    assert list(enum(True)) == []
    with pytest.raises(TypeError):
        enum()

def test__enumerate_01():
    # d = zip(range(10), map(lambda x:x*x, range(10)))
    index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    cc = "ABCDEFGHIJ"
    cm = "abcdefghij"
    c = zip(cc, cm)
    d = dict(c)
    n = 0
    for i, v in ddict.ddict._enumerate(list(cc)):
        assert i == n and v == cc[n]
        n += 1
    n = 0
    for k, v in ddict.ddict._enumerate(d):
        assert k == cc[n] and v == cm[n]
        n +=1

def test_flatten_01():
    assert ddict.ddict.flatten(john) == john_flat

def test_flatten_02():
    assert ddict.ddict.flatten(john, 1) == john_flat1

def test_flatten_03():
    assert ddict.ddict.flatten(john, 2) == john_flat2

def test_flatten_bad_args():
    with pytest.raises(TypeError):
        ddict.ddict.flatten('Jack')
    with pytest.raises(TypeError):
        ddict.ddict.flatten(12)
    with pytest.raises(TypeError):
        ddict.ddict.flatten(12.34)
    with pytest.raises(TypeError):
        ddict.ddict.flatten(True)
    with pytest.raises(TypeError):
        ddict.ddict.flatten(None)
    with pytest.raises(TypeError):
        ddict.ddict.flatten({1, 2, 3})
    with pytest.raises(TypeError):
        ddict.ddict.flatten((1, 2, 3))
    with pytest.raises(TypeError):
        ddict.ddict.flatten([1, 2, 3])


class TestDotAccessDict():

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_constructor01(self):
        a = Dict()
        assert a.to_dict() == {}

    def test_constructor02(self):
        d = {'name': 'Joe', 'age': 18}
        a = Dict(d)
        assert a.to_dict() == d

    def test_constructor03(self):
        d = dict(name='Joe', age=18)
        a = Dict(d)
        assert a.to_dict() == d

    def test_constructor_kwargs_01(self):
        d = dict(name='Joe', age=18)
        a = Dict(name='Joe', age=18)
        assert a.to_dict() == d

    def test_constructor_tuple_01(self):
        d = dict(name='Joe', age=18)
        a = Dict(('name', 'Joe'), ('age',18))
        assert a.to_dict() == d

    def test_constructor_list_of_tuples_01(self):
        d = dict(name='Joe', age=18)
        a = Dict([('name', 'Joe'), ('age',18)])
        assert a.to_dict() == d

    def test_constructor_iterator_zip_01(self):
        l = ['name', 'age', 'sex']
        m = ['John', '38', 'M']
        d = dict(zip(l, m))
        a = Dict(zip(l, m))
        assert a.to_dict() == d

    def test_constructor_exceptions_01(self):
        v1 = '{"name": "Joe", "age": 18}'
        v2 = 123
        v3 = 3.14
        v4 = True
        v5 = None
        with pytest.raises(TypeError):
            a = Dict(v1)
        with pytest.raises(TypeError):
            a = Dict(v2)
        with pytest.raises(TypeError):
            a = Dict(v3)
        with pytest.raises(TypeError):
            a = Dict(v4)
        with pytest.raises(TypeError):
            a = Dict(v5)

    def test_constructor_generator_01(self):
        l = ['name', 'age', 'sex']
        m = ['John', '38', 'M']
        d = dict(zip(l, m))
        def gen1():
            for i, k in enumerate(l):
                yield (k, m[i])
        a = Dict(gen1())
        assert a.to_dict() == d

    def test_update_bad_args(self):
        a = Dict(john)
        v1 = 'John'
        v2 = 123
        v3 = 12.3
        v4 = True
        v5 = None
        v6 = [1, 2, 3]
        v7 = (1, 2, 3)
        with pytest.raises(TypeError):
            a.update(v1)
        with pytest.raises(TypeError):
            a.update(v2)
        with pytest.raises(TypeError):
            a.update(v3)
        with pytest.raises(TypeError):
            a.update(v4)
        with pytest.raises(TypeError):
            a.update(v5)
        with pytest.raises(TypeError):
            a.update(v6)
        with pytest.raises(TypeError):
            a.update(v7)

    def test_update_01(self):
        a = {
          'name': 'A',
          'next': ['B', 'C', 'D']
        }
        b = {
          'next':['E', 'F']
        }
        d = Dict(a)
        d.update(b)
        a.update(b)
        assert d.to_dict() == a

    def test_update_02(self):
        a = {
          'name': 'A',
          'next': {'nodes':['B', 'C', 'D']}
        }
        b = {
          'next':{'nodes':['E', 'F']}
        }
        d = Dict(a)
        d.update(b)
        a.update(b)
        assert d.to_dict() == a
        
    def test_get_01(self):
        d = Dict(john)
        assert d.get('age') == 55
        assert d.get('children[0][0].age') == 18
        assert d.get('children[0][0].brother.age') == 8
        assert d.get('children[0][0].brother.name') == 'Jack'
        assert d.get('children[0][0].brother.sex') == 'M'
        assert d.get('children[0][0].name') == 'Joe'
        assert d.get('children[0][0].sex') == 'M'
        
    def test_set_01(self):
        d = Dict(john)

        assert d.get('age') == 55
        d.set('age', 66)
        assert d.get('age') == 66

        assert d.get('children[0][0].age') == 18
        d.set('children[0][0].age', 29)
        assert d.get('children[0][0].age') == 29

        assert d.get('children[0][0].brother.age') == 8
        d.set('children[0][0].brother.age', 90)
        assert d.get('children[0][0].brother.age') == 90

        assert d.get('children[0][0].brother.name') == 'Jack'
        d.set('children[0][0].brother.name', 'Quba')
        assert d.get('children[0][0].brother.name') == 'Quba'

    def test_dir_01(self):
        d = Dict(john)
        assert set(dir(d)) == {'age', 'children', 'name', 'sex'}

