import inspect
from typing import Callable, List

__SHIFT = '  '


def get_fct_parameter_names(fct: Callable) -> List[str]:
    """
    Returns the list of parameter names from the given function.

    Args:
        fct (Callable): The function to extract parameters from.

    Returns:
        List[str]: The list of parameter names.
    """
    return list(inspect.signature(fct).parameters.keys())


def get_current_fct_filename(level: int = 1) -> str:
    """Return the caller function or method filename

    Args:
        level (int, optional): Index of previous caller. Defaults to 1.

    Returns:
        str: Caller function or method filename
    """
    return inspect.stack()[level][1]


def get_current_fct_line(level: int = 1) -> str:
    """Return the caller function or method line

    Args:
        level (int, optional): Index of previous caller. Defaults to 1.

    Returns:
        str: Caller function or method line
    """
    return inspect.stack()[level][2]


def get_current_fct_name(level: int = 1) -> str:
    """Return the caller function or method name

    Args:
        level (int, optional): Index of previous caller. Defaults to 1.

    Returns:
        str: Caller function or method name
    """
    return inspect.stack()[level][3]


def print_pos(shift: int = 0, suffix: str = '', level: int = 1):
    """Print the caller function or method name with filename and line

    Args:
        shift (int, optional): Shift level. Defaults to 0.
        suffix (str, optional): Suffix string. Defaults to ''.
        level (int, optional): Index of previous caller. Defaults to 1.
    """
    if suffix:
        suffix = ' %s' % suffix
    print("%sFunction '%s' in file '%s', line %s%s\n" % (
          __SHIFT * shift,
          get_current_fct_name(level + 1),
          get_current_fct_filename(level + 1),
          get_current_fct_line(level + 1),
          suffix)
          )
