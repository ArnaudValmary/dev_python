from typing import Any, Dict

from myexec import exec_command


def test_myexec_faulty_ls() -> None:
    exec_return_dict: Dict[str, Any] = exec_command('faulty_ls',
                                                    shell=False)
    # print("output=<%s>" % exec_return_dict)
    assert \
        not exec_return_dict['timeout_flag'] \
        and exec_return_dict['child_exception_flag'] \
        and exec_return_dict['exception'] \
        and exec_return_dict['return_code'] == -1 \
        and not exec_return_dict['stdout_is_string'] \
        and isinstance(exec_return_dict['stdout'], bytes) \
        and not exec_return_dict['stdout'] \
        and exec_return_dict['stderr_is_string'] \
        and isinstance(exec_return_dict['stderr'], str) \
        and not exec_return_dict['stderr']
