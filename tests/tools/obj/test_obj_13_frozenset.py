from tools.obj import objrepr


def test_obj_01_frozenset_empty() -> None:
    r: str = objrepr(frozenset())
    assert r == 'frozenset()'


def test_obj_01_frozenset_level1() -> None:
    r: str = objrepr(frozenset({"1"}), level=1)
    assert r == """    frozenset(
        str(1)
    )"""


def test_obj_01_frozenset_level2() -> None:
    r: str = objrepr(frozenset({1, 1.2}), level=2)
    assert r == """        frozenset(
            float(1.2)
            int(1)
        )"""


def test_obj_01_frozenset_name() -> None:
    r: str = objrepr(frozenset({"1", 2.3}), level=1, name="the_frozenset")
    # print('r=\n%s' % r)
    assert r == """    the_frozenset = frozenset(
        float(2.3)
        str(1)
    )"""


def test_obj_01_frozenset_name_nested() -> None:
    r: str = objrepr(frozenset({1, 1.2, "5", (1, 2)}), level=1, name="the_frozenset")
    # print('r=\n%s' % r)
    # Nested frozenset are not possible because frozenset are not hashable
    assert r == """    the_frozenset = frozenset(
        float(1.2)
        int(1)
        str(5)
        tuple(
            #0 = int(1)
            #1 = int(2)
        )
    )"""
