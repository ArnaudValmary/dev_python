from tools.obj import objrepr


def test_obj_01_set_empty() -> None:
    r: str = objrepr(set())
    assert r == 'set()'


def test_obj_01_set_level1() -> None:
    r: str = objrepr({"1"}, level=1)
    assert r == """    set(
        str(1)
    )"""


def test_obj_01_set_level2() -> None:
    r: str = objrepr({1, 1.2}, level=2)
    assert r == """        set(
            float(1.2)
            int(1)
        )"""


def test_obj_01_set_name() -> None:
    r: str = objrepr({"1", 2.3}, level=1, name="the_set")
    # print('r=\n%s' % r)
    assert r == """    the_set = set(
        float(2.3)
        str(1)
    )"""


def test_obj_01_set_name_nested() -> None:
    r: str = objrepr({1, 1.2, "5", (1, 2)}, level=1, name="the_set")
    # print('r=\n%s' % r)
    # Nested set are not possible because set are not hashable
    assert r == """    the_set = set(
        float(1.2)
        int(1)
        str(5)
        tuple(
            #0 = int(1)
            #1 = int(2)
        )
    )"""
