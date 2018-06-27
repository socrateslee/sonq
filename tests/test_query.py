from sonq.query import get_separated_attr, match

data = [
    {"num": 0,
     "name": "Wang",
     "info": {"attack": 100},
     "logs": [{"type": "login"}],
     "tags": ["sun", "moon"]}
]


def test_get_separated_attr():
    assert get_separated_attr(data[0], "name") == (True, "Wang")
    assert get_separated_attr(data[0], "info.attack") == (True, 100)
    assert get_separated_attr(data[0], "info.not_existed") == (False, None)
    assert get_separated_attr(data[0], "logs.0.not_existed") == (False, None)
    assert get_separated_attr(data[0], "logs.0.type") == (True, "login")
    assert get_separated_attr(data[0], "logs.1.type") == (False, None)


def test_simple_int_equal():
    assert match(data[0], {'num': 0})


def test_simple_int_inequal():
    assert not match(data[0], {'num': 1})


def test_simple_nested_equal():
    assert match(data[0], {'info': {'attack': 100}})


def test_simple_nested_inequal():
    assert not match(data[0], {'info': {'attack': 50}})


def test_simple_separated_equal():
    assert match(data[0], {'info.attack': 100})


def test_simple_separated_inequal():
    assert not match(data[0], {'info.attack': 50})


def test_op_eq():
    assert match(data[0], {'info.attack': {'$eq': 100}})
    assert match(data[0], {'tags': {'$eq': "sun"}})
    assert match(data[0], {'tags': {'$eq': ["sun", "moon"]}})


def test_op_ne():
    assert match(data[0], {'info.attack': {'$ne': 101}})
    assert match(data[0], {'tags': {'$ne': "fogs"}})


def test_op_in():
    assert match(data[0], {'name': {'$in': ['Wang', 'Zhao']}})
    assert match(data[0], {'tags': {'$in': ['sun']}})
    assert match(data[0], {'tags': {'$in': [['sun', 'moon']]}})


def test_op_nin():
    assert match(data[0], {'name': {'$nin': ['Li', 'Qian']}})
    assert match(data[0], {'tags': {'$nin': ['saturn']}})
    assert match(data[0], {'tags': {'$nin': [['saturn', 'ceras']]}})


def test_op_compare():
    assert match(data[0], {'info.attack': {'$gt': 99}})
    assert match(data[0], {'info.attack': {'$gte': 100}})
    assert match(data[0], {'info.attack': {'$lt': 101}})
    assert match(data[0], {'info.attack': {'$lte': 100}})


def test_op_and():
    assert match(data[0], {'$and': [
        {'name': 'Wang'},
        {'num': 0},
        {'info.attack': {'$ne': 102}},
    ]})


def test_op_or():
    assert match(data[0], {'$or': [
        {'name': 'Li'},
        {'num': 2},
        {'info.attack': {'$ne': 102}},
    ]})


def test_op_nor():
    assert match(data[0], {'$nor': [
        {'name': 'Li'},
        {'num': 2},
        {'info.attack': {'$eq': 102}},
    ]})


def test_op_not():
    assert match(data[0], {'$not': 
                           {"name": "Li"}
    })


def test_exists():
    assert match(data[0], {'num': {'$exists': True}})
    assert match(data[0], {'non': {'$exists': False}})
