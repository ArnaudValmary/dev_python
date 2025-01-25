#! /usr/bin/env python

"""
Module for executing functions and tracing back any exceptions.

This module provides a utility function `exec_and_traceback_all_exceptions` that allows you to execute a given
    function while tracing back any exceptions that occur during execution.
    The function will return `True` if no exceptions were raised,
    or the formatted traceback of the last exception encountered.

Functions
----------

.. function:: exec_and_traceback_all_exceptions(fct: Callable, *args, **kwargs) -> Tuple[bool, Any]
    Execute a given function while tracing back any exceptions that occur during execution.

    Args:
        fct (Callable): The function to execute.
        *args: Additional positional arguments to pass to the function.
        **kwargs: Additional keyword arguments to pass to the function.

    Returns:
        Tuple[bool, Any]: A tuple containing a boolean indicating whether an exception was raised,
            and the formatted traceback of the last exception encountered if one was raised, or None otherwise.
"""

import traceback
from typing import Any, Callable, Tuple


def exec_and_traceback_all_exceptions(fct: Callable, *args, **kwargs) -> Tuple[bool, Any]:
    """
    Execute a given function while tracing back any exceptions that occur during execution.

    Args:
        fct (Callable): The function to execute.
        *args: Additional positional arguments to pass to the function.
        **kwargs: Additional keyword arguments to pass to the function.

    Returns:
        Tuple[bool, Any]: A tuple containing a boolean indicating whether an exception was raised,
            and the formatted traceback of the last exception encountered if one was raised, or None otherwise.
    """
    try:
        return (True, fct(*args, **kwargs))
    except Exception:
        return (False, traceback.format_exc())


#
# The lines below are for illustrative purposes only
#
if __name__ == '__main__':
    def fct1(x: int) -> None:
        x += 1
        #  Error!
        "A" + x

    def fct2(x) -> None:
        fct1(x)

    ok: bool = False
    return_value: Any = None
    (ok, return_value) = exec_and_traceback_all_exceptions(fct2, 1)

    if ok:
        print("return value='%s'" % return_value)
    else:
        print("traceback='%s'" % return_value)
