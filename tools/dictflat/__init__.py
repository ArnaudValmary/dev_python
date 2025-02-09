#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import Any, Callable, Dict, Final, List
from uuid import uuid4


def get_uuid() -> str:
    return str(uuid4())


__RE_UPPER_LETTER: Final[re.Pattern[str]] = re.compile(r'(?<!^)(?=[A-Z])')
__RE_MULTIPLE_UNDERSCORE: Final[re.Pattern[str]] = re.compile(r'_+')


def str_2_snakecase(fn: str) -> str:
    return __RE_MULTIPLE_UNDERSCORE.sub('_', __RE_UPPER_LETTER.sub('_', fn).lower())


def __flat(d: Dict,
           flatten_dict: Dict[str, List[Dict[str, Any]]],
           flat_dict_key: str = '',
           fieldname_prefix: str = '',
           current_dict: Dict = None,
           ref_name: str = None,
           ref_value: str = None,
           sep: str = '.',
           id_field_name: str = '__id',
           ref_field_prefix: str = '__ref_',
           snakecase_fieldnames: bool = False,
           rename_values: Dict[str, str] = None,
           rename_list: Dict[str, str] = None,
           filter_values: Dict[str, Callable] = None,
           drop_values: List[str] = None,
           drop_objects: List[str] = None,
           use_nested: bool = True) -> None:

    if snakecase_fieldnames:
        fieldname_prefix = str_2_snakecase(fieldname_prefix)
    if not flat_dict_key:
        flat_dict_key = fieldname_prefix
    elif snakecase_fieldnames:
        flat_dict_key = str_2_snakecase(flat_dict_key)
    if rename_list and flat_dict_key in rename_list:
        flat_dict_key = rename_list[flat_dict_key]

    for field_name in d:
        if flatten_dict.get(flat_dict_key, None) is None:
            flatten_dict[flat_dict_key] = []

        if current_dict is None:
            current_dict: Dict = {}
            current_dict[id_field_name] = get_uuid()
            if ref_name and ref_value:
                current_dict['%s%s' % (ref_field_prefix, ref_name)] = ref_value
            flatten_dict[flat_dict_key].append(current_dict)

        if snakecase_fieldnames:
            field_name_value: str = str_2_snakecase(field_name)
        else:
            field_name_value: str = field_name
        if fieldname_prefix:
            field_name_value = '%s%s%s' % (fieldname_prefix, sep, field_name_value)
        if rename_values and field_name_value in rename_values:
            field_name_value = rename_values[field_name_value]

        field_value: Any = d[field_name]

        if use_nested and isinstance(field_value, dict):
            if not drop_objects or field_name not in drop_objects:
                __flat(field_value,
                       flatten_dict,
                       flat_dict_key=flat_dict_key,
                       fieldname_prefix=field_name_value,
                       current_dict=current_dict,
                       sep=sep,
                       id_field_name=id_field_name,
                       ref_field_prefix=ref_field_prefix,
                       snakecase_fieldnames=snakecase_fieldnames,
                       rename_values=rename_values,
                       rename_list=rename_list,
                       filter_values=filter_values,
                       drop_values=drop_values,
                       drop_objects=drop_objects,
                       use_nested=use_nested)
        elif isinstance(field_value, list) or isinstance(field_value, tuple) or not use_nested and isinstance(field_value, dict):
            if isinstance(field_value, dict):
                field_value = [field_value]
            if not drop_objects or field_name not in drop_objects:
                if len(field_value) > 0 and isinstance(field_value[0], dict):
                    for elt in field_value:
                        __flat(elt,
                               flatten_dict,
                               flat_dict_key=field_name,
                               ref_name=flat_dict_key,
                               ref_value=current_dict[id_field_name],
                               sep=sep,
                               id_field_name=id_field_name,
                               ref_field_prefix=ref_field_prefix,
                               snakecase_fieldnames=snakecase_fieldnames,
                               rename_values=rename_values,
                               rename_list=rename_list,
                               filter_values=filter_values,
                               drop_values=drop_values,
                               drop_objects=drop_objects,
                               use_nested=use_nested)
                else:
                    field_value_bis: List = []
                    for elt in field_value:
                        field_value_bis.append({"%s" % field_name_value: elt})
                    for elt in field_value_bis:
                        __flat(elt,
                               flatten_dict,
                               flat_dict_key=field_name,
                               ref_name=flat_dict_key,
                               ref_value=current_dict[id_field_name],
                               sep=sep,
                               id_field_name=id_field_name,
                               ref_field_prefix=ref_field_prefix,
                               snakecase_fieldnames=snakecase_fieldnames,
                               rename_values=rename_values,
                               rename_list=rename_list,
                               filter_values=filter_values,
                               drop_values=drop_values,
                               drop_objects=drop_objects,
                               use_nested=use_nested)

        else:
            if not drop_values or field_name_value not in drop_values:
                if filter_values and field_name_value in filter_values:
                    current_dict[field_name_value] = filter_values[field_name_value](
                        fieldname=field_name_value,
                        value=field_value
                    )
                else:
                    current_dict[field_name_value] = field_value


def flat(d: Dict,
         flat_dict_key: str,
         sep: str = '.',
         id_field_name: str = '__id',
         ref_field_prefix: str = '__ref__',
         snakecase_fieldnames: bool = False,
         rename_values: Dict[str, str] = None,
         rename_list: Dict[str, str] = None,
         filter_values: Dict[str, Callable] = None,
         drop_values: List[str] = None,
         drop_objects: List[str] = None,
         use_nested: bool = True) -> Dict[str, List[Dict[str, Any]]]:
    flatten_dict: Dict = {}
    __flat(
        d=d,
        flatten_dict=flatten_dict,
        flat_dict_key=flat_dict_key,
        sep=sep,
        id_field_name=id_field_name,
        ref_field_prefix=ref_field_prefix,
        snakecase_fieldnames=snakecase_fieldnames,
        rename_values=rename_values,
        rename_list=rename_list,
        filter_values=filter_values,
        drop_values=drop_values,
        drop_objects=drop_objects,
        use_nested=use_nested
    )
    return flatten_dict


if __name__ == '__main__':

    import datetime
    import json
    import re

    def fix_date(fieldname: str, value: str) -> str:
        return datetime.datetime.strptime(value, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

    d: Dict = {
        "name": "John",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA"
        },
        "address2": {
            "street": "125 Main St",
            "city": "Anytown",
            "state": "CA"
        },
        "phone_numbers": [
            {"type": "home", "number": "555-1234"},
            {"type": "work", "number": "555-5678"}
        ]
    }

    print(
        json.dumps(
            flat(d,
                 flat_dict_key='person',
                 use_nested=False,
                 drop_objects=[
                     'address2',
                 ]),
            indent=2
        )
    )
