from tools.obj import OBJ_LEVEL_BASE, OBJ_PREFIX, objrepr


def test_obj_01_str() -> None:
    r: str = objrepr('1')
    assert r == 'str(1)'


def test_obj_01_str_level1() -> None:
    r: str = objrepr('2', level=1)
    assert r == '%sstr(2)' % (OBJ_LEVEL_BASE)


def test_obj_01_str_level2() -> None:
    r: str = objrepr('-1', level=2)
    assert r == '%sstr(-1)' % (OBJ_LEVEL_BASE * 2)


def test_obj_01_str_name() -> None:
    r: str = objrepr('-3', name='xxx')
    assert r == 'xxx%sstr(-3)' % (OBJ_PREFIX)


def test_obj_01_str_level1_name() -> None:
    r: str = objrepr('15', name='xxx', level=1)
    assert r == '%sxxx%sstr(15)' % (OBJ_LEVEL_BASE, OBJ_PREFIX)
