from myversion import myversion


def test_myversion_01_eq_1() -> None:
    assert myversion("1") == myversion("1")


def test_myversion_01_eq_2() -> None:
    assert myversion("1.2") == myversion("1.02")


def test_myversion_01_eq_3() -> None:
    assert myversion("1.2-4") == myversion("1.2.4")
