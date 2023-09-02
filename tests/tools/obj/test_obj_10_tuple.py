from tools.obj import objrepr


def test_obj_01_tuple_empty() -> None:
    r: str = objrepr(tuple())
    assert r == 'tuple()'


def test_obj_01_tuple_level1() -> None:
    r: str = objrepr((1,), level=1)
    assert r == """    tuple(
        #0 = int(1)
    )"""


def test_obj_01_tuple_level2() -> None:
    r: str = objrepr((1, 1.2), level=2)
    assert r == """        tuple(
            #0 = int(1)
            #1 = float(1.2)
        )"""


def test_obj_01_tuple_name() -> None:
    r: str = objrepr((1, 1.2), level=1, name="the_tuple")
    assert r == """    the_tuple = tuple(
        #0 = int(1)
        #1 = float(1.2)
    )"""


def test_obj_01_tuple_name_nested() -> None:
    r: str = objrepr((1, 1.2, (2, 2.1), (3, (4, 4.1))), level=1, name="the_tuple")
    # print('r=\n%s' % r)
    assert r == """    the_tuple = tuple(
        #0 = int(1)
        #1 = float(1.2)
        #2 = tuple(
            #0 = int(2)
            #1 = float(2.1)
        )
        #3 = tuple(
            #0 = int(3)
            #1 = tuple(
                #0 = int(4)
                #1 = float(4.1)
            )
        )
    )"""
