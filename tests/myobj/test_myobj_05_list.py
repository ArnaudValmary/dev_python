from myobj import myrepr


def test_myobj_01_list_empty() -> None:
    r: str = myrepr([])
    assert r == 'list()'


def test_myobj_01_list_level1() -> None:
    r: str = myrepr([1], level=1)
    assert r == """    list(
        #0 = int(1)
    )"""


def test_myobj_01_list_level2() -> None:
    r: str = myrepr([1, 1.2], level=2)
    assert r == """        list(
            #0 = int(1)
            #1 = float(1.2)
        )"""


def test_myobj_01_list_name() -> None:
    r: str = myrepr([1, 1.2], level=1, name="the_list")
    assert r == """    the_list = list(
        #0 = int(1)
        #1 = float(1.2)
    )"""


def test_myobj_01_list_name_nested() -> None:
    r: str = myrepr([1, 1.2, [2, 2.1], [3, [4, 4.1]]], level=1, name="the_list")
    # print('r=\n%s' % r)
    assert r == """    the_list = list(
        #0 = int(1)
        #1 = float(1.2)
        #2 = list(
            #0 = int(2)
            #1 = float(2.1)
        )
        #3 = list(
            #0 = int(3)
            #1 = list(
                #0 = int(4)
                #1 = float(4.1)
            )
        )
    )"""
