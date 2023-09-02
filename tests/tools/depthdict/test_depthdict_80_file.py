import json

from tools.depthdict import depthdict


def test_file_write_read() -> None:
    d_w = depthdict({'a': 'letter a'})
    d_w > "./tmp/a.json"
    d_r = depthdict()
    d_r < "./tmp/a.json"
    assert d_w == d_r


def test_file_write2_read() -> None:
    d_w = depthdict({'a': 'letter a'})
    d_w > "./tmp/a.json"
    d_w >> "./tmp/a.json"
    d_r = depthdict()
    try:
        d_r < "./tmp/a.json"
        assert False
    except json.decoder.JSONDecodeError:
        assert True


def test_file_write_read_update() -> None:
    d_w = depthdict({'a': 'letter a'})
    d_w > "./tmp/a.json"
    d_r = depthdict({'b': 'letter b'})
    d_r << "./tmp/a.json"
    assert {'a': 'letter a', 'b': 'letter b'} == d_r
