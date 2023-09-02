from tools.obj import OBJ_LEVEL_BASE, OBJ_PREFIX, objrepr


def test_obj_01_none() -> None:
    r: str = objrepr(None)
    assert r == 'None'


def test_obj_01_none_level1() -> None:
    r: str = objrepr(None, level=1)
    assert r == '%sNone' % (OBJ_LEVEL_BASE)


def test_obj_01_none_level2() -> None:
    r: str = objrepr(None, level=2)
    assert r == '%sNone' % (OBJ_LEVEL_BASE * 2)


def test_obj_01_none_name() -> None:
    r: str = objrepr(None, name='xxx')
    assert r == 'xxx%sNone' % OBJ_PREFIX


def test_obj_01_none_level1_name() -> None:
    r: str = objrepr(None, name='xxx', level=1)
    assert r == '%sxxx%sNone' % (OBJ_LEVEL_BASE, OBJ_PREFIX)
