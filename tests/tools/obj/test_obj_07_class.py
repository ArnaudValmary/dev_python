from tools.obj import objrepr


class A:
    def __init__(self):
        pass


def test_obj_01_class_empty() -> None:
    a = A()
    r: str = objrepr(a)
    # print("<%s>" % r)
    assert r == 'class(A) = attributes()'


def test_obj_01_class_level1() -> None:
    a = A()
    a.attr_1 = 1
    r: str = objrepr(a, level=1)
    assert r == """    class(A) = attributes(
        <attr_1> = int(1)
    )"""


def test_obj_01_class_level2() -> None:
    a = A()
    a.attr_1 = 1
    a.attr_2 = 'v_b'
    r: str = objrepr(a, level=2)
    assert r == """        class(A) = attributes(
            <attr_1> = int(1)
            <attr_2> = str(v_b)
        )"""


def test_obj_01_class_name() -> None:
    a = A()
    a.attr_4 = 1
    a.attr_5 = 1.2
    r: str = objrepr(a, level=1, name="the_class")
    # print('r=\n%s' % r)
    assert r == """    the_class = class(A) = attributes(
        <attr_4> = int(1)
        <attr_5> = float(1.2)
    )"""


def test_obj_01_class_name_nested() -> None:
    a = A()
    c = A()
    d = A()
    d_2 = A()
    a.attr_a = 1
    a.attr_b = 1.2
    a.attr_c = c
    a.attr_c = d
    c.attr_c_1 = 2
    c.attr_c_2 = 2.1
    d.attr_d_1 = 3
    d.attr_d_2 = d_2
    d_2.attr_d_2_1 = 4
    d_2.attr_d_2_2 = 4.1
    r: str = objrepr(a, name="the_class")
    # print("<%s>" % r)
    assert r == """the_class = class(A) = attributes(
    <attr_a> = int(1)
    <attr_b> = float(1.2)
    <attr_c> = class(A) = attributes(
        <attr_d_1> = int(3)
        <attr_d_2> = class(A) = attributes(
            <attr_d_2_1> = int(4)
            <attr_d_2_2> = float(4.1)
        )
    )
)"""
