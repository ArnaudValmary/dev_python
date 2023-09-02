import yaml

from tools.obj import objrepr


def f(i: int, s: str) -> str:
    """_summary_

    Args:
        i (int): _description_
        s (str): _description_

    Returns:
        str: _description_
    """
    return s * i


the_obj = [1, "2", {"a": 5}]

print("%s" % objrepr(the_obj))

print("YAML:\n%s" % yaml.dump(the_obj))
