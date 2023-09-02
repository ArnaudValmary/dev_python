from tools.version import version


def test_myversion_01_eq_1() -> None:
    assert version("1") == version("1")


def test_myversion_01_eq_2() -> None:
    assert version("1.2") == version("1.02")


def test_myversion_01_eq_3() -> None:
    assert version("1.2-4") == version("1.2.4")
