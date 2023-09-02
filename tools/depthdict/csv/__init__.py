#! /usr/bin/env python

"""This is a test for transform data records (dictionnaries from JSON for example) into CSV files and compressed with Zip
"""

import csv
from io import BytesIO, StringIO
from typing import Any, Dict, List
from zipfile import ZipFile

from tools.depthdict import depthdict


def flat_dicts(ld: List[Dict],
               fd_key: str,
               sep: str = '.',
               id_field_name: str = '__id',
               ref_field_prefix: str = '__ref__') -> Dict[str, List[Dict[str, Any]]]:
    """Flatten a list of dictionaries into several dictionary lists for transformation into CSV files.
    :param ld: List of dictionnaries
    :param fd_key: Root name
    :returns: A dictionnary of list of flatten dictionnaries
    """
    fd: Dict[str, List[Dict[str, Any]]] = {}
    for elt in ld:
        md = depthdict(elt)
        md.flat(fd_key=fd_key, fd=fd,
                sep=sep,
                id_field_name=id_field_name,
                ref_field_prefix=ref_field_prefix)
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
    """Create in memory CSV contents from field names and dictionnaries

    :param fieldnames_dict: Dictionnary of list of field names
    :param records_dict: Dictionnary of list of records (dictionnaries)
    :param dialect: Output format
    :param delimiter: Output fields separator
    :returns: Dictionnary of CSV contents and filenames
    """
    if not dialect:
        dialect = 'excel'
    if not delimiter:
        delimiter = ','
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


def create_csv_files_from_dict_list(dict_list: List[Dict],
                                    fd_key: str,
                                    sep: str = '.',
                                    id_field_name: str = '__id',
                                    ref_field_prefix: str = '__ref__',
                                    csv_dialect: str = 'excel',
                                    csv_delimiter: str = ','
                                    ) -> Dict[str, Dict[str, str]]:
    """Create in memory CSV contents from dictionnary list

    :param dict_list: list of dictionnaries (records)
    :param fd_key: Root name
    :param dialect: CSV Output format
    :param delimiter: CSV output fields separator
    :returns: Dictionnary of CSV contents and filenames
    """
    # Flat records
    records_dict: Dict[str, List[Dict[str, Any]]] = flat_dicts(dict_list,
                                                               fd_key=fd_key,
                                                               sep=sep,
                                                               id_field_name=id_field_name,
                                                               ref_field_prefix=ref_field_prefix)

    # Build fieldnames
    fieldnames_dict: Dict[str, List[str]] = build_field_lists(records_dict)

    # Create CSV files
    csv_files: Dict[str, Dict[str, str]] = create_csv_files(fieldnames_dict,
                                                            records_dict,
                                                            dialect=csv_dialect,
                                                            delimiter=csv_delimiter)
    return csv_files


def create_zip_files(files: Dict[str, Dict[str, str]],
                     internal_dir_name: str = None) -> bytes:
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
    return zip_bytes_in_memory.getvalue()
