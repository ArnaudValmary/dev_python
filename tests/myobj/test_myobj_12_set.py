from myobj import myrepr


def test_myobj_01_set_empty() -> None:
    r: str = myrepr(set())
    assert r == 'set()'


def test_myobj_01_set_level1() -> None:
    r: str = myrepr({"1"}, level=1)
    assert r == """    set(
        str(1)
    )"""


def test_myobj_01_set_level2() -> None:
    r: str = myrepr({1, 1.2}, level=2)
    assert r == """        set(
            float(1.2)
            int(1)
        )"""


def test_myobj_01_set_name() -> None:
    r: str = myrepr({"1", 2.3}, level=1, name="the_set")
    # print('r=\n%s' % r)
    assert r == """    the_set = set(
        float(2.3)
        str(1)
    )"""


def test_myobj_01_set_name_nested() -> None:
    r: str = myrepr({1, 1.2, "5", (1, 2)}, level=1, name="the_set")
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
