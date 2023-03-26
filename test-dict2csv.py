#! /usr/bin/env python

"""This is a test for transform data records (dictionnaries from JSON for example) into CSV files and compressed with Zip
"""

import csv
import json
from typing import Any, Dict, List
from uuid import uuid4 as get_uuid
from io import StringIO, BytesIO
from zipfile import ZipFile


def flat_dict(d: Dict[str, Any],
              fd: Dict[str, List[Dict[str, Any]]], fd_key: str = '',
              prefix: str = '',
              record: Dict = None,
              ref_name: str = None,
              ref_value: str = None,
              sep: str = '.') -> None:
    """Flatten a dictionary into several dictionary lists for transformation into CSV files.
    :param d: The original dictionnary
    :param fd: A dictionnary of list of flatten dictionnaries
    :param sep: Separator used to build concatenate new field names
    """
    if not fd_key:
        fd_key: str = prefix
        # print("init fd_key with prefix=<%s>" % fd_key)

    if isinstance(d, Dict):
        for field_name in d:
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
                record['__id'] = str(get_uuid())
                if ref_name and ref_value:
                    record['__ref__%s' % ref_name] = ref_value
                fd[fd_key].append(record)
                # print('  init record=<%s> and add it to fd[fd_key=<%s>] list' % (record, fd_key))

            field_name_value: str = field_name
            if prefix:
                field_name_value = prefix + sep + field_name_value

            field_value: Any = d[field_name]

            if isinstance(field_value, Dict):
                # print("  sub:%s" % field_name)
                flat_dict(d[field_name],
                          fd, fd_key=fd_key,
                          prefix=field_name_value,
                          record=record,
                          sep=sep)
            elif isinstance(field_value, List):
                for elt in d[field_name]:
                    flat_dict(elt,
                              fd, fd_key=field_name,
                              ref_name=fd_key, ref_value=record['__id'],
                              sep=sep)
            else:
                # print("  append field: <%s>=<%s>" % (field_name_value, field_value))
                record[field_name_value] = field_value


def flat_dicts(ld: List[Dict], fd_key: str = None) -> Dict[str, List[Dict[str, Any]]]:
    """Flatten a list of dictionaries into several dictionary lists for transformation into CSV files.
    :param ld: List of dictionnaries
    :param fd_key: Root name
    :returns: A dictionnary of list of flatten dictionnaries
    """
    fd: Dict[str, List[Dict[str, Any]]] = {}
    for elt in ld:
        flat_dict(elt, fd, fd_key=fd_key)
    return fd


def build_field_list(el: List[Dict[str, Any]]) -> List[str]:
    """Build the list of fields from a list of flatten dictionnaries
    :param el: List of flatten dictionnaries
    :returns: List of field names
    """
    field_names: set[str] = set()
    for elt in el:
        field_names = field_names.union(elt.keys())
    # print("set=<%s>", field_names)
    field_names_list = list(field_names)
    field_names_list.sort()
    return field_names_list


def build_field_lists(fd: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[str]]:
    """Build lists of fields from a dictionnary of list of flatten dictionnaries
    Necessary for building first line of CSV files (field names)

    :param fd: Dictionnary of list of flattent dictionnaries
    :returns: Dictionnary of list of field names
    """
    dh: Dict[List[str]] = {}
    for fd_key in fd:
        dh[fd_key] = build_field_list(fd[fd_key])
    return dh


def create_csv_file_from_list(fieldnames: List[str],
                              records: List[Dict],
                              dialect: str = 'excel',
                              delimiter: str = ',') -> str:
    """Create a CSV content

    :param fieldnames: List of field names
    :param records: List of records (dictionnaries)
    :param dialect: Output format
    :param delimiter: Output fields separator
    :returns: CSV content
    """
    string_file_in_memory = StringIO()
    writer: csv.DictWriter = csv.DictWriter(string_file_in_memory,
                                            fieldnames=fieldnames,
                                            extrasaction='ignore',
                                            dialect=dialect,
                                            delimiter=delimiter)
    writer.writeheader()
    for record in records:
        writer.writerow(record)
    return string_file_in_memory.getvalue()


def create_csv_files(fieldnames_dict: Dict[str, List[str]],
                     records_dict: Dict[str, List[Dict[str, Any]]],
                     dialect: str = 'excel',
                     delimiter: str = ',') -> Dict[str, Dict[str, str]]:
    """Create a CSV content

    :param fieldnames_dict: Dictionnary of list of field names
    :param records_dict: Dictionnary of list of records (dictionnaries)
    :param dialect: Output format
    :param delimiter: Output fields separator
    :returns: Dictionnary of CSV contents and filenames
    """
    csv_files: Dict[str, str] = {}
    for type_name in fieldnames_dict:
        csv_files[type_name] = {
            'content': create_csv_file_from_list(fieldnames_dict[type_name],
                                                 records_dict[type_name],
                                                 dialect=dialect,
                                                 delimiter=delimiter),
            'file_name': '%s.csv' % (type_name),
        }
    return csv_files


def create_zip_files(files: Dict[str, Dict[str, str]],
                     internal_dir_name: str = None) -> memoryview:
    """Create Zip files from CSV contents and filenames

    :param files: Dictionnary of CSV contents and filenames
    :param internal_dir_name: inernal directory name
    :returns: Zip file content
    """
    zip_bytes_in_memory: BytesIO = BytesIO()
    zipfile = ZipFile(zip_bytes_in_memory, mode='w')
    for type_name in files:
        file: Dict[str, str] = files[type_name]
        full_file_name: str = file['file_name']
        if internal_dir_name:
            full_file_name = '/'.join([internal_dir_name, full_file_name])
        zipfile.writestr('%s' % (full_file_name), data=file['content'])
    zipfile.close()
    return zip_bytes_in_memory.getbuffer()


# Two dictionnaries
d1: Dict = {
    'a': 1,
    'b': {
        'b1': 1,
        'b2': 2,
        'c': {
            'cx': 'CX',
        },
    },
    'extra_info': [
        {"a": 1},
        {
            "b": 2,
            "c": 3,
            "d": {
                "d1": "dede",
            }
        },
        {
            "list": [
                {
                    "elt1": "value1",
                }
            ]
        }
    ]
}
d2: Dict = {
    'a': 2,
    'b': {
        'b1': 3,
        'b2': 4,
        'c': {
            'cy': 'CY',
        },
    },
    'extra_info': [
        {"a": 5},
        {
            "b": 7,
            "c": 8,
            "d": {
                "d1": "efef",
            }
        },
        {
            "list": [
                {
                    "elt9": "value9",
                }
            ]
        }
    ]
}

print("json(d1)=<%s>" % (json.dumps(d1, indent=2)))
print("json(d2)=<%s>" % (json.dumps(d2, indent=2)))

# List of records
records: List[Dict[str, Any]] = [d1, d2]

# Flat records
records_dict: Dict[str, List[Dict[str, Any]]] = flat_dicts(records, fd_key="pReFiX")
print("json(records_dict)=<%s>" % (json.dumps(records_dict, indent=2)))

# Build fieldnames
fieldnames_dict: Dict[str, List[str]] = build_field_lists(records_dict)
print("fieldnames_dict=<%s>" % (json.dumps(fieldnames_dict, indent=2)))

# Create CSV files
csv_files: Dict[str, Dict[str, str]] = create_csv_files(fieldnames_dict,
                                                        records_dict,
                                                        dialect='excel',
                                                        delimiter=',')

# Create Zip file
dir_name: str = "yo"
zip_buffer: Any = create_zip_files(csv_files, internal_dir_name=dir_name)

# Check result with a real file
zip_name: str = 'test.zip'
with open(zip_name, mode='bw') as zip_file:
    zip_file.write(zip_buffer)
    zip_file.close()
