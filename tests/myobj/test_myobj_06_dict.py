from myobj import myrepr


def test_myobj_01_dict_empty() -> None:
    r: str = myrepr({})
    assert r == 'dict()'


def test_myobj_01_dict_level1() -> None:
    r: str = myrepr({'a': 1}, level=1)
    assert r == """    dict(
        <a> = int(1)
    )"""


def test_myobj_01_dict_level2() -> None:
    r: str = myrepr({'a': 1, 'b': 'v_b'}, level=2)
    assert r == """        dict(
            <a> = int(1)
            <b> = str(v_b)
        )"""


def test_myobj_01_dict_name() -> None:
    r: str = myrepr({4: 1, 5: 1.2}, level=1, name="the_dict")
    assert r == """    the_dict = dict(
        <4> = int(1)
        <5> = float(1.2)
    )"""


def test_myobj_01_dict_name_nested() -> None:
    r: str = myrepr({'a': 1, 'b': 1.2, 'c': {'c.1': 2, 'c.2': 2.1}, 'd': {'d.1': 3, 'd.2': {'d.2.1': 4, 'd.2.2': 4.1}}}, name="the_dict")
    assert r == """the_dict = dict(
    <a> = int(1)
    <b> = float(1.2)
    <c> = dict(
        <c.1> = int(2)
        <c.2> = float(2.1)
    )
    <d> = dict(
        <d.1> = int(3)
        <d.2> = dict(
            <d.2.1> = int(4)
            <d.2.2> = float(4.1)
        )
    )
)"""
