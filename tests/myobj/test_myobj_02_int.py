from myobj import MYOBJ_LEVEL_BASE, MYOBJ_PREFIX, myrepr


def test_myobj_01_int() -> None:
    r: str = myrepr(1)
    assert r == 'int(1)'


def test_myobj_01_int_level1() -> None:
    r: str = myrepr(2, level=1)
    assert r == '%sint(2)' % (MYOBJ_LEVEL_BASE)


def test_myobj_01_int_level2() -> None:
    r: str = myrepr(-1, level=2)
    assert r == '%sint(-1)' % (MYOBJ_LEVEL_BASE * 2)


def test_myobj_01_int_name() -> None:
    r: str = myrepr(-3, name='xxx')
    assert r == 'xxx%sint(-3)' % (MYOBJ_PREFIX)


def test_myobj_01_int_level1_name() -> None:
    r: str = myrepr(15, name='xxx', level=1)
    assert r == '%sxxx%sint(15)' % (MYOBJ_LEVEL_BASE, MYOBJ_PREFIX)
