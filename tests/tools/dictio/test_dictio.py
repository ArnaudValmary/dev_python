import json

from tools.dictio import DictIO


def test_file_write_read() -> None:
    d_w = DictIO({'a': 'letter a'})
    d_w > "./tmp/a.json"
    d_r = DictIO()
    d_r < "./tmp/a.json"
    assert d_w == d_r


def test_file_write2_read() -> None:
    d_w = DictIO({'a': 'letter a'})
    d_w > "./tmp/a.json"
    d_w >> "./tmp/a.json"
    d_r = DictIO()
    try:
        d_r < "./tmp/a.json"
        assert False
    except json.decoder.JSONDecodeError:
        assert True


def test_file_write_read_update() -> None:
    d_w = DictIO({'a': 'letter a'})
    d_w > "./tmp/a.json"
    d_r = DictIO({'b': 'letter b'})
    d_r << "./tmp/a.json"
    assert {'a': 'letter a', 'b': 'letter b'} == d_r
