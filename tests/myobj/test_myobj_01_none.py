from myobj import MYOBJ_LEVEL_BASE, MYOBJ_PREFIX, myrepr


def test_myobj_01_none() -> None:
    r: str = myrepr(None)
    assert r == 'None'


def test_myobj_01_none_level1() -> None:
    r: str = myrepr(None, level=1)
    assert r == '%sNone' % (MYOBJ_LEVEL_BASE)


def test_myobj_01_none_level2() -> None:
    r: str = myrepr(None, level=2)
    assert r == '%sNone' % (MYOBJ_LEVEL_BASE * 2)


def test_myobj_01_none_name() -> None:
    r: str = myrepr(None, name='xxx')
    assert r == 'xxx%sNone' % (MYOBJ_PREFIX)


def test_myobj_01_none_level1_name() -> None:
    r: str = myrepr(None, name='xxx', level=1)
    assert r == '%sxxx%sNone' % (MYOBJ_LEVEL_BASE, MYOBJ_PREFIX)
