#! /usr/bin/env python

"""This is a test for dictionnary extension and funny use cases
"""

import json
import re
from typing import Any, Dict, List, Union
from uuid import uuid4 as get_uuid


def get_str_sorted_list_elem(lst: List, *args, **kw) -> List:
    return sorted(lst, key=str, reverse=kw.get('reverse', False))


def get_int_sorted_list_elem(lst: List, *args, **kw) -> List:
    return sorted(lst, key=int, reverse=kw.get('reverse', False))


class depthdict(dict):
    def __init__(self, *args, **kw) -> None:
        super(depthdict, self).__init__(*args, **kw)

    def to_json(self) -> str:
        return json.dumps(self)

    def _flat(self,
              fd: Dict[str, List[Dict[str, Any]]],
              fd_key: str = '',
              prefix: str = '',
              record: Dict = None,
              ref_name: str = None,
              ref_value: str = None,
              sep: str = '.',
              id_field_name: str = '__id',
              ref_field_prefix: str = '__ref_') -> None:
        if not fd_key:
            fd_key: str = prefix
            # print("init fd_key with prefix=<%s>" % fd_key)

        for field_name in self:
            # print('field_name=<%s>' % field_name)
            if fd.get(fd_key, None) is None:
                fl: List[Dict[str, Any]] = []
                fd[fd_key] = fl
                # print('  init fd[fd_key<%s>] (fl) with empty list' % fd_key)
            else:
                fl: List[Dict[str, Any]] = fd[fd_key]
                # print('  fl in fd_key<%s> with = <%s>' % (fd_key, fl))

            if record is None:
                record: Dict = {}
                record[id_field_name] = str(get_uuid())
                if ref_name and ref_value:
                    record['%s%s' % (ref_field_prefix, ref_name)] = ref_value
                fd[fd_key].append(record)
                # print('  init record=<%s> and add it to fd[fd_key=<%s>] list' % (record, fd_key))

            field_name_value: str = field_name
            if prefix:
                field_name_value = prefix + sep + field_name_value

            field_value: Any = self[field_name]

            if isinstance(field_value, depthdict):
                # print("  sub:%s" % field_name)
                field_value._flat(fd, fd_key=fd_key,
                                  prefix=field_name_value,
                                  record=record,
                                  sep=sep,
                                  id_field_name=id_field_name,
                                  ref_field_prefix=ref_field_prefix)
            elif isinstance(field_value, Dict):
                # print("  sub:%s" % field_name)
                depthdict(field_value)._flat(fd, fd_key=fd_key,
                                             prefix=field_name_value,
                                             record=record,
                                             sep=sep,
                                             id_field_name=id_field_name,
                                             ref_field_prefix=ref_field_prefix)
            elif isinstance(field_value, List):
                for elt in self[field_name]:
                    depthdict(elt)._flat(fd, fd_key=field_name,
                                         ref_name=fd_key, ref_value=record[id_field_name],
                                         sep=sep,
                                         id_field_name=id_field_name,
                                         ref_field_prefix=ref_field_prefix)
            else:
                # print("  append field: <%s>=<%s>" % (field_name_value, field_value))
                record[field_name_value] = field_value

    def flat(self,
             fd_key: str,
             fd: Dict[str, List[Dict[str, Any]]] = None,
             sep: str = '.',
             id_field_name: str = '__id',
             ref_field_prefix: str = '__ref__') -> Dict[str, List[Dict[str, Any]]]:
        """Flatten a dictionary into several dictionary lists for transformation into CSV files.
        :param fd_key: Root name
        :param fd: Previous flat call return
        :param sep: Separator used to build concatenate new field names
        :param field_id_name:
        :returns: A dictionnary of list of flatten dictionnaries
        """
        if fd is None:
            fd = {}
        self._flat(fd=fd,
                   fd_key=fd_key,
                   sep=sep,
                   id_field_name=id_field_name,
                   ref_field_prefix=ref_field_prefix)
        return fd

    def get_int_sorted_keys(self, *args, **kw) -> List:
        return get_int_sorted_list_elem(list(self.keys()), key=int, *args, **kw)

    def get_str_sorted_keys(self, *args, **kw) -> List:
        return get_str_sorted_list_elem(list(self.keys()), key=str, *args, **kw)

    def get_depth(self,
                  f: Union[List[str], str] = None,
                  d: str = None,
                  s: str = '.'
                  ) -> Any:
        field_names: List[str] = []
        if f is None or not f:
            return d
        elif isinstance(f, str):
            if s:
                field_names = f.split(s)
            else:
                field_names = [f]
        elif isinstance(f, list):
            field_names = f
        else:
            return d
        len_fields_minus_one: int = len(field_names) - 1
        c_d: Any = self
        for i, field_name in enumerate(field_names):
            flag_list: bool = False
            z: re.Match[str] | None = re.match(
                r'^(?P<field_name>[^[]+)\[(?P<list_index>-?[0-9]+)\]$',
                field_name)
            if z is not None:
                flag_list = True
                field_name: str = z.group('field_name')
                list_index: int = int(z.group('list_index'))
                # print("I=<%d>" % list_index)
            if field_name in c_d:
                if i == len_fields_minus_one:
                    if flag_list:
                        if isinstance(c_d[field_name], List):
                            # print("LIST")
                            if (list_index >= 0 and list_index >= len(c_d[field_name])) or \
                               (list_index < 0 and -list_index > len(c_d[field_name])):
                                # print("  OOB")
                                return d
                            else:
                                return c_d[field_name][list_index:][0]
                        else:
                            return d
                    else:
                        return c_d[field_name]
                else:
                    if flag_list:
                        if isinstance(c_d[field_name], List):
                            if (list_index >= 0 and list_index >= len(c_d[field_name])) or \
                               (list_index < 0 and -list_index > len(c_d[field_name])):
                                return d
                            else:
                                c_d = c_d[field_name][list_index:][0]
                        else:
                            return d
                    else:
                        c_d = c_d[field_name]
            else:
                return d

    def set_depth(self,
                  f: Union[List[str], str] = None,
                  v: Any = None,
                  s: str = '.',
                  add_in_list: bool = False,
                  uniq: bool = False
                  ) -> Any:
        field_names: List[str] = []
        if f is None or not f:
            return self
        elif isinstance(f, str):
            if s:
                field_names = f.split(s)
            else:
                field_names = [f]
        elif isinstance(f, list):
            field_names = f
        else:
            return self
        len_fields_minus_one: int = len(field_names) - 1
        d: Any = self
        for i, field_name in enumerate(field_names):
            if i < len_fields_minus_one:
                if field_name not in d or not isinstance(d, dict):
                    d[field_name] = {}
                d = d[field_name]
            else:
                if add_in_list:
                    if field_name not in d or not isinstance(d[field_name], list):
                        d[field_name] = []
                    if not uniq or field_name not in d:
                        d[field_name].append(v)
                    break
                else:
                    d[field_name] = v
                    break
        return self

    def __gt__(self, other) -> None:
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "w") as f:
            f.write("%s\n" % (json.dumps(self)))

    def __rshift__(self, other) -> None:
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "a") as f:
            f.write("%s\n" % (json.dumps(self)))

    def __lt__(self, other) -> None:
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "r") as f:
            self.clear()
            self.update(json.loads(f.read()))

    def __lshift__(self, other) -> None:
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "r") as f:
            self.update(json.loads(f.read()))
