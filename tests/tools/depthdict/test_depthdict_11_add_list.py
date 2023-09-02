from tools.depthdict import depthdict


def test_01_set_depth_add_in_list_1() -> None:
    d = depthdict({})
    d.set_depth(f='a', v='letter a in list', add_in_list=True)
    assert d == {'a': ['letter a in list']}


def test_01_set_depth_add_in_list_1_double() -> None:
    d = depthdict({})
    d.set_depth(f='a', v='letter a in list', add_in_list=True)
    d.set_depth(f='a', v='letter a in list', add_in_list=True)
    assert d == {'a': ['letter a in list', 'letter a in list']}


def test_01_set_depth_add_in_list_2() -> None:
    d = depthdict({})
    d.set_depth(f='a', v='letter a in list', add_in_list=True)
    d.set_depth(f='a', v='letter b in list', add_in_list=True)
    assert d == {'a': ['letter a in list', 'letter b in list']}


def test_01_set_depth_add_in_list_3_uniq() -> None:
    d = depthdict({})
    d.set_depth(f='a', v='letter a in list', add_in_list=True)
    d.set_depth(f='a', v='letter a in list', add_in_list=True, uniq=True)
    assert d == {'a': ['letter a in list']}
