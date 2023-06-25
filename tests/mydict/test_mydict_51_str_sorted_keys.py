from mydict import mydict


def test_get_str_sorted_keys() -> None:
    d = mydict({'1': "one"})
    d['5'] = "five"
    d['10'] = "ten"
    d['2'] = "two"
    d['15'] = "fiveteen"
    assert d.get_str_sorted_keys() == ['1', '10', '15', '2', '5']
