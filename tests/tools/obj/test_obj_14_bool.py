from tools.obj import OBJ_LEVEL_BASE, OBJ_PREFIX, objrepr


def test_obj_01_bool_true() -> None:
    r: str = objrepr(True)
    assert r == 'True'


def test_obj_01_bool_false() -> None:
    r: str = objrepr(False)
    assert r == 'False'


def test_obj_01_bool_level1() -> None:
    r: str = objrepr(True, level=1)
    assert r == '%sTrue' % (OBJ_LEVEL_BASE)


def test_obj_01_bool_level2() -> None:
    r: str = objrepr(False, level=2)
    assert r == '%sFalse' % (OBJ_LEVEL_BASE * 2)


def test_obj_01_bool_name() -> None:
    r: str = objrepr(True, name='xxx')
    assert r == 'xxx%sTrue' % (OBJ_PREFIX)


def test_obj_01_bool_level1_name() -> None:
    r: str = objrepr(False, name='xxx', level=1)
    assert r == '%sxxx%sFalse' % (OBJ_LEVEL_BASE, OBJ_PREFIX)
