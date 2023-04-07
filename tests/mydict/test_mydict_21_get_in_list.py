from mydict import mydict


def test_01_get_list() -> None:
    d = mydict({})
    d.set_depth(f='a', v='zero', add_in_list=True)
    d.set_depth(f='a', v='one', add_in_list=True)
    assert d.get_depth('a') == ['zero', 'one']


def test_01_get_inlist_0() -> None:
    d = mydict({})
    d.set_depth(f='a', v='zero', add_in_list=True)
    assert d.get_depth('a[0]') == 'zero'


def test_01_get_inlist_1() -> None:
    d = mydict({})
    d.set_depth(f='a', v='zero', add_in_list=True)
    d.set_depth(f='a', v='one', add_in_list=True)
    assert d.get_depth('a[1]') == 'one'


def test_01_get_inlist_oob() -> None:
    d = mydict({})
    d.set_depth(f='a', v='zero', add_in_list=True)
    assert d.get_depth('a[1]') is None


def test_01_get_inlist_m1() -> None:
    d = mydict({})
    d.set_depth(f='a', v='m1', add_in_list=True)
    assert d.get_depth('a[-1]') == 'm1'


def test_01_get_inlist_m2() -> None:
    d = mydict({})
    d.set_depth(f='a', v='m2', add_in_list=True)
    d.set_depth(f='a', v='m1', add_in_list=True)
    assert d.get_depth('a[-2]') == 'm2'


def test_01_get_inlist_oob_neg() -> None:
    d = mydict({})
    d.set_depth(f='a', v='zero', add_in_list=True)
    assert d.get_depth('a[-2]') is None


def test_01_get_inlist_0_sub() -> None:
    d = mydict({})
    d.set_depth(f='a', v={'x': '0'}, add_in_list=True)
    assert d.get_depth('a[0].x') == '0'


def test_01_get_inlist_1_sub() -> None:
    d = mydict({})
    d.set_depth(f='a', v={'x': '0'}, add_in_list=True)
    d.set_depth(f='a', v={'x': '1'}, add_in_list=True)
    assert d.get_depth('a[1].x') == '1'


def test_01_get_inlist_oob_sub() -> None:
    d = mydict({})
    d.set_depth(f='a', v={'x': '0'}, add_in_list=True)
    assert d.get_depth('a[1].x') is None


def test_01_get_inlist_m1_sub() -> None:
    d = mydict({})
    d.set_depth(f='a', v={'x': '-1'}, add_in_list=True)
    assert d.get_depth('a[-1].x') == '-1'


def test_01_get_inlist_m2_sub() -> None:
    d = mydict({})
    d.set_depth(f='a', v={'x': '-2'}, add_in_list=True)
    d.set_depth(f='a', v={'x': '-1'}, add_in_list=True)
    assert d.get_depth('a[-2].x') == '-2'


def test_01_get_inlist_oob_neg_sub() -> None:
    d = mydict({})
    d.set_depth(f='a', v={'x': '-1'}, add_in_list=True)
    assert d.get_depth('a[-2].x') is None
