from tools.obj import OBJ_LEVEL_BASE, OBJ_PREFIX, objrepr


def test_obj_01_bytearray_true() -> None:
    r: str = objrepr(bytearray(2))
    assert r == 'bytearray(b\'\\x00\\x00\')'


def test_obj_01_bytearray_level1() -> None:
    r: str = objrepr(bytearray(2), level=1)
    assert r == '%sbytearray(b\'\\x00\\x00\')' % (OBJ_LEVEL_BASE)


def test_obj_01_bytearray_level2() -> None:
    r: str = objrepr(bytearray(2), level=2)
    assert r == '%sbytearray(b\'\\x00\\x00\')' % (OBJ_LEVEL_BASE * 2)


def test_obj_01_bytearray_name() -> None:
    r: str = objrepr(bytearray(2), name='xxx')
    assert r == 'xxx%sbytearray(b\'\\x00\\x00\')' % (OBJ_PREFIX)


def test_obj_01_bytearray_level1_name() -> None:
    r: str = objrepr(bytearray(2), name='xxx', level=1)
    assert r == '%sxxx%sbytearray(b\'\\x00\\x00\')' % (OBJ_LEVEL_BASE, OBJ_PREFIX)
