from myobj import MYOBJ_LEVEL_BASE, MYOBJ_PREFIX, myrepr


def test_myobj_01_bytearray_true() -> None:
    r: str = myrepr(bytearray(2))
    assert r == 'bytearray(b\'\\x00\\x00\')'


def test_myobj_01_bytearray_level1() -> None:
    r: str = myrepr(bytearray(2), level=1)
    assert r == '%sbytearray(b\'\\x00\\x00\')' % (MYOBJ_LEVEL_BASE)


def test_myobj_01_bytearray_level2() -> None:
    r: str = myrepr(bytearray(2), level=2)
    assert r == '%sbytearray(b\'\\x00\\x00\')' % (MYOBJ_LEVEL_BASE * 2)


def test_myobj_01_bytearray_name() -> None:
    r: str = myrepr(bytearray(2), name='xxx')
    assert r == 'xxx%sbytearray(b\'\\x00\\x00\')' % (MYOBJ_PREFIX)


def test_myobj_01_bytearray_level1_name() -> None:
    r: str = myrepr(bytearray(2), name='xxx', level=1)
    assert r == '%sxxx%sbytearray(b\'\\x00\\x00\')' % (MYOBJ_LEVEL_BASE, MYOBJ_PREFIX)
