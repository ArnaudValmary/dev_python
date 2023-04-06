from mydict import mydict


def test_get_int_sorted_keys() -> None:
    d = mydict({1: "one"})
    d[5] = "five"
    d[10] = "ten"
    d[2] = "two"
    d[15] = "fiveteen"
    assert d.get_int_sorted_keys(reverse=True) == [15, 10, 5, 2, 1]
