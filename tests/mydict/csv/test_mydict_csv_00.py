import json
from typing import Any, Dict, List
import mydict.csv


def test_dict_list_2_zip() -> None:
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

    csv_files: Dict[str, Dict[str, str]] = mydict.csv.create_csv_files_from_dict_list(records, "root")
    print("json(csv_files)=<%s>" % (json.dumps(csv_files, indent=2)))

    assert csv_files

    # Create Zip file
    dir_name: str = "dirname"
    zip_buffer: bytes = mydict.csv.create_zip_files(csv_files, internal_dir_name=dir_name)

    assert zip_buffer

    # Check result with a real file
    zip_name: str = './tmp/test.zip'
    with open(zip_name, mode='bw') as zip_file:
        zip_file.write(zip_buffer)
        zip_file.close()
