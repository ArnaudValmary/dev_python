from tools.obj import OBJ_LEVEL_BASE, OBJ_PREFIX, objrepr


def test_obj_01_complex() -> None:
    r: str = objrepr(1j)
    assert r == 'complex(0.0+1.0j)'


def test_obj_01_complex_zero() -> None:
    r: str = objrepr(1+0j)
    assert r == 'complex(1.0+0.0j)'


def test_obj_01_complex_level1() -> None:
    r: str = objrepr(2+3j, level=1)
    assert r == '%scomplex(2.0+3.0j)' % (OBJ_LEVEL_BASE)


def test_obj_01_complex_level2() -> None:
    r: str = objrepr(-1.2+5.1j, level=2)
    assert r == '%scomplex(-1.2+5.1j)' % (OBJ_LEVEL_BASE * 2)


def test_obj_01_complex_name() -> None:
    r: str = objrepr(10+5j, name='the_complex')
    assert r == 'the_complex%scomplex(10.0+5.0j)' % (OBJ_PREFIX)


def test_obj_01_complex_level1_name() -> None:
    r: str = objrepr(150-11.7j, name='the_complex', level=1)
    assert r == '%sthe_complex%scomplex(150.0-11.7j)' % (OBJ_LEVEL_BASE, OBJ_PREFIX)
