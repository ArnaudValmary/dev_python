from myobj import MYOBJ_LEVEL_BASE, MYOBJ_PREFIX, myrepr


def test_myobj_01_bytes() -> None:
    r: str = myrepr(b'1')
    assert r == "b'1'"


def test_myobj_01_bytes_2() -> None:
    r: str = myrepr(bytes(1))
    assert r == "b'\\x00'"


def test_myobj_01_bytes_level1() -> None:
    r: str = myrepr(b'2', level=1)
    assert r == "%sb'2'" % (MYOBJ_LEVEL_BASE)


def test_myobj_01_bytes_level2() -> None:
    r: str = myrepr(b'-1', level=2)
    assert r == "%sb'-1'" % (MYOBJ_LEVEL_BASE * 2)


def test_myobj_01_bytes_name() -> None:
    r: str = myrepr(b'-3', name='xxx')
    assert r == "xxx%sb'-3'" % (MYOBJ_PREFIX)


def test_myobj_01_bytes_level1_name() -> None:
    r: str = myrepr(b'15', name='xxx', level=1)
    assert r == "%sxxx%sb'15'" % (MYOBJ_LEVEL_BASE, MYOBJ_PREFIX)
