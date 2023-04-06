from typing import Any, Dict
from myexec import exec_command

gv_input: str = """
digraph G {
    Hello -> World
}
"""


def test_myexec_output_str() -> None:
    exec_return_dict: Dict[str, Any] = exec_command('dot -Tsvg',
                                                    stdin=gv_input,
                                                    convert_stdout_to_string=True)
    # print("output=<%s>" % exec_return_dict)
    assert not exec_return_dict['timeout_flag'] \
           and not exec_return_dict['child_exception_flag'] \
           and not exec_return_dict['exception'] \
           and exec_return_dict['return_code'] == 0 \
           and exec_return_dict['stdout_is_string'] \
           and isinstance(exec_return_dict['stdout'], str) \
           and exec_return_dict['stdout'] \
           and exec_return_dict['stderr_is_string'] \
           and isinstance(exec_return_dict['stderr'], str) \
           and not exec_return_dict['stderr']
