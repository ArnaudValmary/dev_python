from tools.depthdict import depthdict


def test_init_01_empty() -> None:
    d = depthdict({})
    assert d == {}


def test_init_02_one() -> None:
    d = depthdict({'one': 1})
    assert d == {
        'one': 1
    }


def test_init_02_two() -> None:
    d = depthdict({
        'one': 1,
        'two': '2'
    })
    assert d == {
        'two': '2',
        'one': 1
    }
