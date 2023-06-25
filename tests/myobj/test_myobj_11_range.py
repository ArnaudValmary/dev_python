from myobj import MYOBJ_LEVEL_BASE, MYOBJ_PREFIX, myrepr


def test_myobj_01_range() -> None:
    r: str = myrepr(range(1))
    assert r == 'range(0, 1, 1)'


def test_myobj_01_range_level1() -> None:
    r: str = myrepr(range(2), level=1)
    assert r == '%srange(0, 2, 1)' % (MYOBJ_LEVEL_BASE)


def test_myobj_01_range_level2() -> None:
    r: str = myrepr(range(3, 10), level=2)
    assert r == '%srange(3, 10, 1)' % (MYOBJ_LEVEL_BASE * 2)


def test_myobj_01_range_name() -> None:
    r: str = myrepr(range(4, 12, 2), name='xxx')
    assert r == 'xxx%srange(4, 12, 2)' % (MYOBJ_PREFIX)


def test_myobj_01_range_level1_name() -> None:
    r: str = myrepr(range(-1, -15, -3), name='xxx', level=1)
    assert r == '%sxxx%srange(-1, -15, -3)' % (MYOBJ_LEVEL_BASE, MYOBJ_PREFIX)
