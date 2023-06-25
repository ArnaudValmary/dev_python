from myobj import MYOBJ_LEVEL_BASE, MYOBJ_PREFIX, myrepr


def test_myobj_01_float() -> None:
    r: str = myrepr(1.0)
    assert r == 'float(1.0)'


def test_myobj_01_float_level1() -> None:
    r: str = myrepr(2.1, level=1)
    assert r == '%sfloat(2.1)' % (MYOBJ_LEVEL_BASE)


def test_myobj_01_float_level2() -> None:
    r: str = myrepr(-1.65, level=2)
    assert r == '%sfloat(-1.65)' % (MYOBJ_LEVEL_BASE * 2)


def test_myobj_01_float_name() -> None:
    r: str = myrepr(-3.935, name='xxx')
    assert r == 'xxx%sfloat(-3.935)' % (MYOBJ_PREFIX)


def test_myobj_01_float_level1_name() -> None:
    r: str = myrepr(15.12345, name='xxx', level=1)
    assert r == '%sxxx%sfloat(15.12345)' % (MYOBJ_LEVEL_BASE, MYOBJ_PREFIX)
