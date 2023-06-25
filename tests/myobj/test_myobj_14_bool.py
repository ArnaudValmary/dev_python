from myobj import MYOBJ_LEVEL_BASE, MYOBJ_PREFIX, myrepr


def test_myobj_01_bool_true() -> None:
    r: str = myrepr(True)
    assert r == 'True'


def test_myobj_01_bool_false() -> None:
    r: str = myrepr(False)
    assert r == 'False'


def test_myobj_01_bool_level1() -> None:
    r: str = myrepr(True, level=1)
    assert r == '%sTrue' % (MYOBJ_LEVEL_BASE)


def test_myobj_01_bool_level2() -> None:
    r: str = myrepr(False, level=2)
    assert r == '%sFalse' % (MYOBJ_LEVEL_BASE * 2)


def test_myobj_01_bool_name() -> None:
    r: str = myrepr(True, name='xxx')
    assert r == 'xxx%sTrue' % (MYOBJ_PREFIX)


def test_myobj_01_bool_level1_name() -> None:
    r: str = myrepr(False, name='xxx', level=1)
    assert r == '%sxxx%sFalse' % (MYOBJ_LEVEL_BASE, MYOBJ_PREFIX)
