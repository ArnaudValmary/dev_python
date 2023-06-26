from myversion import myversion


def test_myversion_02_lt_1() -> None:
    assert myversion("1") < myversion("1.0")


def test_myversion_02_lt_2() -> None:
    assert myversion("1.1") < myversion("1.02")


def test_myversion_02_lt_3() -> None:
    assert myversion("1.2-4") < myversion("1.2.5")
