#! /usr/bin/env python

"""Simple test program to execute commands in sub-process"""

import subprocess
from typing import Any, Dict, Union


def exec_command(cmd: str,
                 stdin: Union[bytes, str] = None,
                 stdin_encoding: str = 'UTF-8',
                 timeout_seconds: int = 10,
                 convert_stdout_to_string: bool = False,
                 stdout_encoding: str = 'UTF-8',
                 convert_stderr_to_string: bool = True,
                 stderr_encoding: str = 'UTF-8',
                 shell: bool = True) -> Dict[str, Any]:
    """Execute a command in a subprocess
    :param stdin: Bytes or string input data
    :param stdin_encoding: if stdin is string type, use this encoding to convert in bytes type
    :param timeout_seconds: execution timeout in seconds
    :param convert_stdout_to_string: convert stdout into a string
    :param stdout_encoding: use the encoding to convert stdout in string type
    :param convert_stderr_to_string: convert stderr into a string
    :param stderr_encoding: use the encoding to convert stderr in string type
    :param shell: use sub-shell to execute command
    :returns: A dictionnary with all information
    """
    stdin_bytes: bytes = b''
    if isinstance(stdin, bytes):
        stdin_bytes = stdin
    elif isinstance(stdin, str):
        stdin_bytes = bytes(stdin, encoding=stdin_encoding)

    out_bytes: bytes = b''
    err_bytes: bytes = b''
    timeout_flag: bool = False
    return_code: int = -1
    child_exception_flag: bool = False
    sp: subprocess.Popen = None
    exception: Exception = None
    try:
        sp = subprocess.Popen(cmd,
                              shell=shell,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    except Exception as e:
        child_exception_flag = True
        exception = str(e)
    if not exception:
        try:
            (out_bytes, err_bytes) = sp.communicate(input=stdin_bytes, timeout=timeout_seconds)
        except subprocess.TimeoutExpired as spte:
            timeout_flag = True
            exception = str(spte)
    if not timeout_flag and not child_exception_flag:
        return_code = sp.returncode
    if convert_stdout_to_string:
        out_bytes = str(out_bytes, encoding=stdout_encoding)
    if convert_stderr_to_string:
        err_bytes = str(err_bytes, encoding=stderr_encoding)
    return {
        'timeout_flag': timeout_flag,
        'child_exception_flag': child_exception_flag,
        'exception': exception,
        'return_code': return_code,
        'stdout_is_string': convert_stdout_to_string,
        'stdout': out_bytes,
        'stderr_is_string': convert_stderr_to_string,
        'stderr': err_bytes,
    }
