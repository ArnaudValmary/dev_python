from tools.obj import OBJ_LEVEL_BASE, OBJ_PREFIX, objrepr


def test_obj_01_bytes() -> None:
    r: str = objrepr(b'1')
    assert r == "b'1'"


def test_obj_01_bytes_2() -> None:
    r: str = objrepr(bytes(1))
    assert r == "b'\\x00'"


def test_obj_01_bytes_level1() -> None:
    r: str = objrepr(b'2', level=1)
    assert r == "%sb'2'" % (OBJ_LEVEL_BASE)


def test_obj_01_bytes_level2() -> None:
    r: str = objrepr(b'-1', level=2)
    assert r == "%sb'-1'" % (OBJ_LEVEL_BASE * 2)


def test_obj_01_bytes_name() -> None:
    r: str = objrepr(b'-3', name='xxx')
    assert r == "xxx%sb'-3'" % (OBJ_PREFIX)


def test_obj_01_bytes_level1_name() -> None:
    r: str = objrepr(b'15', name='xxx', level=1)
    assert r == "%sxxx%sb'15'" % (OBJ_LEVEL_BASE, OBJ_PREFIX)
