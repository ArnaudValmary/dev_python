from myobj import MYOBJ_LEVEL_BASE, MYOBJ_PREFIX, myrepr


def test_myobj_01_str() -> None:
    r: str = myrepr('1')
    assert r == 'str(1)'


def test_myobj_01_str_level1() -> None:
    r: str = myrepr('2', level=1)
    assert r == '%sstr(2)' % (MYOBJ_LEVEL_BASE)


def test_myobj_01_str_level2() -> None:
    r: str = myrepr('-1', level=2)
    assert r == '%sstr(-1)' % (MYOBJ_LEVEL_BASE * 2)


def test_myobj_01_str_name() -> None:
    r: str = myrepr('-3', name='xxx')
    assert r == 'xxx%sstr(-3)' % (MYOBJ_PREFIX)


def test_myobj_01_str_level1_name() -> None:
    r: str = myrepr('15', name='xxx', level=1)
    assert r == '%sxxx%sstr(15)' % (MYOBJ_LEVEL_BASE, MYOBJ_PREFIX)
