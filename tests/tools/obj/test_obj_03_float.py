from tools.obj import OBJ_LEVEL_BASE, OBJ_PREFIX, objrepr


def test_obj_01_float() -> None:
    r: str = objrepr(1.0)
    assert r == 'float(1.0)'


def test_obj_01_float_level1() -> None:
    r: str = objrepr(2.1, level=1)
    assert r == '%sfloat(2.1)' % (OBJ_LEVEL_BASE)


def test_obj_01_float_level2() -> None:
    r: str = objrepr(-1.65, level=2)
    assert r == '%sfloat(-1.65)' % (OBJ_LEVEL_BASE * 2)


def test_obj_01_float_name() -> None:
    r: str = objrepr(-3.935, name='xxx')
    assert r == 'xxx%sfloat(-3.935)' % (OBJ_PREFIX)


def test_obj_01_float_level1_name() -> None:
    r: str = objrepr(15.12345, name='xxx', level=1)
    assert r == '%sxxx%sfloat(15.12345)' % (OBJ_LEVEL_BASE, OBJ_PREFIX)
