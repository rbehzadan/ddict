import json
import pytest

import ddict
import ddict.ddict

Dict = ddict.DotAccessDict


data01 = """
{"menu": {
  "id": "file",
  "value": "File",
  "popup": {
    "menuitem": [
      {"value": "New", "onclick": "CreateNewDoc()"},
      {"value": "Open", "onclick": "OpenDoc()"},
      {"value": "Close", "onclick": "CloseDoc()"}
    ]
  }
}}
"""
data01_flat = '{"menu.id": "file", "menu.value": "File", "menu.popup.menuitem[0].value": "New", "menu.popup.menuitem[0].onclick": "CreateNewDoc()", "menu.popup.menuitem[1].value": "Open", "menu.popup.menuitem[1].onclick": "OpenDoc()", "menu.popup.menuitem[2].value": "Close", "menu.popup.menuitem[2].onclick": "CloseDoc()"}'

data02 = """
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
data02_flat = '{"families.members[0][0]": "Ricardo", "families.members[0][1]": "Alexis", "families.members[0][2]": "Victor", "families.members[1][0][0]": "Shanaya", "families.members[1][0][1]": "Sherry", "families.members[1][1]": "Mary", "families.members[1][2]": "Mateo", "families.members[1][3]": "Zoe", "families.family1": "O\'Barian", "families.family2": "Solloway", "proxies[0].http": "192.168.0.1:8080", "proxies[0].https": "192.168.0.1:8081", "proxies[1].http": "192.168.1.1:8080", "proxies[1].https": "192.168.1.1:8081", "proxies[2][0]": "192.168.2.1", "proxies[2][1]": "192.168.3.1", "proxies[2][2]": "192.168.4.1", "proxies[2][3]": "192.168.5.1", "proxies[2][4]": "192.168.6.1", "proxies[2][5]": "192.168.7.1", "databases.mongodb.url": "mongodb://localhost:27017", "databases.mongodb.host": "localhost", "databases.mongodb.port": 27017, "databases.mongodb.username": "user", "databases.mongodb.password": "pass", "databases.redis.url": "redis://localhost"}'

data = [data01, data02]
flats = [data01_flat, data02_flat]


def test1():
    q={'reza':12, '123':24, (1,2):11}
    with pytest.raises(TypeError):
        ddict.ddict._flatten(q)

def test2():
    with pytest.raises(TypeError):
        ddict.ddict._flatten(data02)

class TestDotAccessDict():

    def setup(self):
        self.data = list(map(json.loads, data))
        self.flats = list(map(json.loads, flats))

    def teardown(self):
        # print("\n*** Teardown ***")
        return

    def test1(self):
        a = self.data[0]['menu']['id']
        assert a == 'file'

    def test2(self):
        a = self.data[0]['menu']['id']
        d = Dict(self.data[0])
        assert d.menu.id == a

    def test3(self):
        for d, f in zip(self.data, self.flats):
            m = Dict(d)
        assert f == m.flatten()

    def test4(self):
        a = Dict(self.data[1])
        s = a.get('families.members[1][0][0]')
        assert s == 'Shanaya'

    def test5(self):
        a = Dict(self.data[1])
        a.set('families.members[1][0][0]', 'Shiva')
        s = a.get('families.members[1][0][0]')
        assert s == 'Shiva'

    def test6(self):
        a = Dict(self.data[1])
        s = a['families']['members'][1][0][0]
        assert s == 'Shanaya'

    def test7(self):
        a = Dict(self.data[1])
        assert 'databases' in a
        assert 'members' not in a

    def test8(self):
        a = Dict(self.data[1])
        assert a.families.members[1][0][0] == 'Shanaya'

    def test9(self):
        with pytest.raises(TypeError):
            a = Dict(data02)

    def test10(self):
        a = Dict(self.data[1])
        with pytest.raises(TypeError):
            a.update(data02)

    def test11(self):
        a = Dict(self.data[1])
        with pytest.raises(SyntaxError):
            a.get('families..members')

    def test12(self):
        a = Dict(self.data[1])
        assert a.databases.mongodb.port == 27017
        a.databases.mongodb.port = 1515
        assert a.databases.mongodb.port == 1515
        assert a['databases']['mongodb']['port'] == 1515
        assert a.get('databases.mongodb.port') == 1515
        a.set('databases.mongodb.port', 1717)
        assert a.databases.mongodb.port == 1717


    def test13(self):
        a = Dict(self.data[1])
        d = a.to_dict()
        assert d == self.data[1]

    def test14(self):
        a = Dict(self.data[1])
        assert dir(a) == ['databases', 'families', 'proxies']

    def test15(self):
        a = Dict(self.data[0])
        b = Dict(self.data[1])
        a.update(b)
        self.data[0].update(self.data[1])
        assert self.data[0] == a

    def test16(self):
        a = Dict(self.data[1])
        assert a.get('families.members[1][0][4]') == None

    def test17(self):
        a = Dict(self.data[1])
        with pytest.raises(SyntaxError):
            a.set('families..members', 'reza')

    def test18(self):
        a = Dict()
        a.person.name = 'Jack'
        a.person.age = 18
        assert a.person == dict(name='Jack', age=18)

