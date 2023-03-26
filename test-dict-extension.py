#! /usr/bin/env python

"""This is a test for dictionnary extension and funny use cases
"""

import json
from typing import Any, List


class my_dict(dict):
    def __init__(self, *args, **kw) -> None:
        super(my_dict, self).__init__(*args, **kw)

    def to_json(self) -> str:
        return json.dumps(self)

    def get_int_sorted_keys(self, *args, **kw) -> List:
        return sorted(self.keys(), key=int, *args, **kw)

    def get_depth(self,
                  f: List[Any] = None,
                  p: str = None,
                  s: str = '.',
                  d: str = None
                  ) -> Any:
        if f is None or not f:
            if p is None or not p:
                return d
            else:
                f: List[Any] = p.split(s)
        len_fields_minus_1: int = len(f) - 1
        d: Any = self
        for i, field in enumerate(f):
            if isinstance(d, dict) and field in d:
                if i < len_fields_minus_1:
                    d = d[field]
                else:
                    return d[field]
            else:
                return d

    def set_depth(self,
                  f: List[str] = None,
                  p: str = None,
                  s: str = '.',
                  v: Any = None
                  ) -> Any:
        if f is None or not f:
            if p is None or not p:
                return self
            else:
                f: List[str] = p.split(s)
        field: str = f[0]
        len_fields_minus_1: int = len(f) - 1
        d: Any = self
        for i, field in enumerate(f):
            if i < len_fields_minus_1:
                if not isinstance(d, dict) or field not in d:
                    d[field] = {}
                d = d[field]
            else:
                d[field] = v
        return self

    def __gt__(self, other) -> bool:
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "w") as f:
            f.write("%s\n" % (json.dumps(self)))

    def __ge__(self, other) -> bool:
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "a") as f:
            f.write("%s\n" % (json.dumps(self)))

    def __lt__(self, other) -> bool:
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "r") as f:
            self.update(json.loads(f.read()))


d = my_dict({1: "one"})
d[5] = "five"
d[10] = "ten"
d[2] = "two"
d[15] = {"a": "a letter", "b": {"c": "b and c letter"}}

print("%s" % (d.to_json()))

print("K[int]=%s" % (d.get_int_sorted_keys(reverse=True)))

print("<%s>" % d.get_depth([1]))
print("<%s>" % d.get_depth([15, "b", "c", "d"], d="xxx"))

d = my_dict()
print("%s" % d)
d.set_depth(["one"], v="the one")
d.set_depth(["two", "three"], v="the two and three")
d.set_depth(["two", "three"], v="the two and three second")
d.set_depth(["one"], v="the one second")
d.set_depth([1, 2, 3], v="o t t")
print("%s" % d)

d > "x.json"
# d >= "x.json"

e = my_dict()
e < "x.json"
print("<%s>" % e)