from tools.depthdict import depthdict


def test_01_set_depth_1() -> None:
    d = depthdict({})
    d.set_depth(f='a', v='letter a')
    assert d == {
        'a': 'letter a'
    }


def test_02_set_depth_1() -> None:
    d = depthdict({})
    d.set_depth(f=['a'], v='letter a')
    assert d == {
        'a': 'letter a'
    }


def test_10_set_depth_2() -> None:
    d = depthdict({})
    d.set_depth(f='a.b', v='letter b')
    assert d == {
        'a': {
            'b': 'letter b'
        }
    }


def test_11_set_depth_2() -> None:
    d = depthdict({})
    d.set_depth(f='a.b', v='letter b')
    d.set_depth(f=['a', 'c'], v='letter c')
    assert d == {
        'a': {
            'b': 'letter b',
            'c': 'letter c'
        }
    }


def test_12_set_depth_3() -> None:
    d = depthdict({})
    d.set_depth(f='a.b', v='letter b')
    d.set_depth(f=['a', 'c', 'e'], v='letter e')
    d.set_depth(f=['b', 'd'], v='letter d')
    assert d == {
        'a': {
            'b': 'letter b',
            'c': {
                'e': 'letter e'
            }
        },
        'b': {
            'd': 'letter d'
        }
    }


def test_20_set_depth_s_1() -> None:
    d = depthdict({})
    d.set_depth(f='a/b', v='letter b', s='/')
    d.set_depth(f='a/c/e', v='letter e', s='/')
    d.set_depth(f='b/d', v='letter d', s='/')
    assert d == {
        'a': {
            'b': 'letter b',
            'c': {
                'e': 'letter e'
            }
        },
        'b': {
            'd': 'letter d'
        }
    }


def test_20_set_depth_s_2() -> None:
    d = depthdict({})
    d.set_depth(f='a##b', v='letter b', s='##')
    d.set_depth(f='a##c##e', v='letter e', s='##')
    d.set_depth(f='b##d', v='letter d', s='##')
    assert d == {
        'a': {
            'b': 'letter b',
            'c': {
                'e': 'letter e'
            }
        },
        'b': {
            'd': 'letter d'
        }
    }
