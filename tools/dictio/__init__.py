#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DictIO Tool
-----------

This tool provides a simple way to manipulate dictionaries by reading, writing,
and updating them using file operations.

Classes and Methods
-------------------

### DictIO

A class used to interact with dictionaries through file operations.

 Attributes:
    d (dict): The dictionary being manipulated.

Methods:
    `__gt__(other: str)`: Writes the current dictionary to a file.
        Examples:
            ```
            # Write the dictionary to a new file named 'data.json'
            DictIO({'name': 'John', 'age': 30}) > 'data.json'
            ```

    `__rshift__(other: str)`: Appends the current dictionary to an existing
        file.
        Examples:
            ```
            # Append the dictionary to an existing file named 'data.json'
            DictIO({'name': 'John', 'age': 30}) >> 'data.json'
            ```

    `__lt__(other: str) -> dict`: Reads a dictionary from a file and returns it.
        Examples:
            ```
            # Read the dictionary from a new file named 'data.json'
            dictio = DictIO() < 'data.json'
            # Returns {'name': 'John', 'age': 30}

    `__lshift__(other: str) -> dict`: Updates the current dictionary with values
        from an existing file.
        Examples:
            ```
            # Update the dictionary with values from an existing file named 'data.json'
            dictio = DictIO({'name': 'John', 'age': 30}) << 'data.json'
            # Returns {'name': 'John', 'age': 30, 'occupation': 'Developer'}

    """

import json
from typing import Dict, Optional


class DictIO():
    def __init__(self, d: Optional[Dict] = None) -> None:
        """
        Initializes a new instance of the `DictIO` class.

        Args:
            d (Optional[Dict]): The dictionary being manipulated. Defaults to an empty
                dictionary if not provided.
        """
        if d is None:
            d = {}
        self.d: Dict = d

    def __gt__(self, other: str) -> None:
        """
        Writes the current dictionary to a file.

        Args:
            other (str): The path to the file where the dictionary will be written.
        Raises:
            Exception: If the provided value is not a string.
        """
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "w") as f:
            f.write("%s\n" % (json.dumps(self.d)))

    def __rshift__(self, other: str) -> None:
        """
        Appends the current dictionary to an existing file.

        Args:
            other (str): The path to the file where the dictionary will be appended.
        Raises:
            Exception: If the provided value is not a string.
        """
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "a") as f:
            f.write("%s\n" % (json.dumps(self.d)))

    def __lt__(self, other: str) -> Dict:
        """
        Reads a dictionary from a file and returns it.

        Args:
            other (str): The path to the file where the dictionary will be read.
        Returns:
            Dict: The dictionary read from the file.
        Raises:
            Exception: If the provided value is not a string.
        """
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "r") as f:
            self.d = {}
            self.d.update(json.loads(f.read()))
            return self.d

    def __lshift__(self, other: str) -> Dict:
        """
        Updates the current dictionary with values from an existing file.

        Args:
            other (str): The path to the file where the values will be read.
        Returns:
            Dict: The updated dictionary.
        Raises:
            Exception: If the provided value is not a string.
        """
        if not isinstance(other, str):
            raise Exception("'%s' is not a string" % (other))
        with open(other, "r") as f:
            self.d.update(json.loads(f.read()))
            return self.d

    def __repr__(self) -> str:
        """
        Returns a string representation of the object, suitable for debugging.

        Args:
            self (dictio): The object to be represented.

        Returns:
            str: A JSON-formatted string representation of the dictionary, with indentation.
        """
        return json.dumps(self.d, indent=2)

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the object.

        Args:
            self (dictio): The object to be represented.

        Returns:
            str: A JSON-formatted string representation of the dictionary.
        """
        return self.__repr__()


if __name__ == '__main__':
    # Create an instance of DictIO
    dictio = DictIO({'name': 'John', 'age': 30})

    print("Original Dictionary:")
    print(dictio)

    # Write the dictionary to a file named 'data.json'
    print("\nWriting dictionary to 'data.json'...")
    dictio > 'data.json'
    # {
    #   "name": "John",
    #   "age": 30
    # }

    # Read the dictionary from the file 'data.json'
    print("\nReading dictionary from 'data.json'...")
    read_dict: Dict = DictIO({'occupation': 'Developer'}) < 'data.json'
    print(read_dict)
    # {'name': 'John', 'age': 30}

    # Update the dictionary with values from the file 'data.json'
    print("\nUpdating dictionary with values from 'data.json'...")
    updated_dict: Dict = DictIO({'occupation': 'Developer'}) << 'data.json'
    print(updated_dict)
    # {'occupation': 'Developer', 'name': 'John', 'age': 30}
