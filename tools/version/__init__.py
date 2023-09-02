import re
from functools import total_ordering
from typing import List


@total_ordering
class version():
    def __init__(self, version: str = '') -> None:
        self.version_list: List[str] = re.split(r'[\.-]', version)
        self.version_len: int = len(self.version_list)

    def __repr__(self) -> str:
        return "version(%d, %s)" % (self.version_len, self.version_list)

    def compare(self, __value: object) -> int:
        assert isinstance(__value, str) or isinstance(__value, version)
        # print("Compare<%s>to<%s>" % (self, __value))
        if isinstance(__value, str):
            __value = version(__value)
        idx: int = 0
        while idx < max(self.version_len, __value.version_len):
            # print("  Idx=%d" % idx)
            if idx >= self.version_len:
                return -1
            if idx >= __value.version_len:
                return 1
            i_version_1: int = -1
            i_version_2: int = -1
            try:
                i_version_1 = int(self.version_list[idx])
                i_version_2 = int(__value.version_list[idx])
            except ValueError:
                pass
            if i_version_1 == -1 or i_version_2 == -1:
                if self.version_list[idx] < __value.version_list[idx]:
                    return -1
                elif self.version_list[idx] > __value.version_list[idx]:
                    return 1
            else:
                if i_version_1 < i_version_2:
                    return -1
                elif i_version_1 > i_version_2:
                    return 1
            idx += 1
        return 0

    def __eq__(self, __value: object) -> bool:
        return self.compare(__value) == 0

    def __ne__(self, __value: object) -> bool:
        return self.compare(__value) != 0

    def __lt__(self, __value: object) -> bool:
        return self.compare(__value) < 0

    def __le__(self, __value: object) -> bool:
        return self.compare(__value) <= 0

    def __gt__(self, __value: object) -> bool:
        return self.compare(__value) > 0

    def __ge__(self, __value: object) -> bool:
        return self.compare(__value) >= 0
