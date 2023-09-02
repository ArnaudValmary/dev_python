from tools.version import version


def test_version_02_lt_1() -> None:
    assert version("1") < version("1.0")


def test_version_02_lt_2() -> None:
    assert version("1.1") < version("1.02")


def test_version_02_lt_3() -> None:
    assert version("1.2-4") < version("1.2.5")
