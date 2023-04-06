from mydict import mydict


def test_01_get_depth_1() -> None:
    d = mydict({})
    d.set_depth(f='a', v='letter a')
    assert d.get_depth('a') == 'letter a'


def test_02_get_depth_1() -> None:
    d = mydict({})
    d.set_depth(f=['a'], v='letter a')
    assert d.get_depth('a') == 'letter a'


def test_10_get_depth_2() -> None:
    d = mydict({})
    d.set_depth(f='a.b', v='letter b')
    assert d.get_depth('a.b') == 'letter b'


def test_11_get_depth_2() -> None:
    d = mydict({})
    d.set_depth(f='a.b', v='letter b')
    d.set_depth(f=['a', 'c'], v='letter c')
    assert d.get_depth(['a', 'c']) == 'letter c'


def test_12_get_depth_3() -> None:
    d = mydict({})
    d.set_depth(f='a.b', v='letter b')
    d.set_depth(f=['a', 'c', 'e'], v='letter e')
    d.set_depth(f=['b', 'd'], v='letter d')
    assert d.get_depth(['a', 'c', 'e']) == 'letter e'


def test_20_get_depth_s_1() -> None:
    d = mydict({})
    d.set_depth(f='a/b', v='letter b', s='/')
    d.set_depth(f='a/c/e', v='letter e', s='/')
    d.set_depth(f='b/d', v='letter d', s='/')
    assert d.get_depth('a/c/e', s='/') == 'letter e'


def test_20_get_depth_s_2() -> None:
    d = mydict({})
    d.set_depth(f='a##b', v='letter b', s='##')
    d.set_depth(f='a##c##e', v='letter e', s='##')
    d.set_depth(f='b##d', v='letter d', s='##')
    assert d.get_depth('a##c##e', s='##') == 'letter e'


def test_30_get_depth_d() -> None:
    d = mydict({})
    assert d.get_depth('a', d='default') == 'default'
