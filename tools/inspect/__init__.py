import inspect
import logging
from typing import Callable, Final, List

full_qual:                 Final[bool] = True
not_full_qual:             Final[bool] = False

default_path_and_name_sep: Final[str] = '.'

__inspect_fct_filename_index: Final[int] = 1
__inspect_fct_line_index:     Final[int] = 2
__inspect_fct_name_index:     Final[int] = 3

logger: logging.Logger = logging.getLogger('Inspect')


def get_fct_name(fct: Callable, full_qual: bool = not_full_qual) -> str:
    if full_qual:
        return fct.__qualname__
    else:
        return fct.__name__


def get_fct_filename(fct: Callable) -> str:
    src_filename: str = None
    try:
        src_filename = inspect.getsourcefile(fct)
    except TypeError:
        src_filename = 'built-in'
    return src_filename


def get_full_fct_path_and_name(fct: Callable, full_qual: bool = not_full_qual, sep=default_path_and_name_sep) -> str:
    return '%s%s%s' % (get_fct_filename(fct), sep, get_fct_name(fct, full_qual))


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
    return inspect.stack()[level][__inspect_fct_filename_index]


def get_current_fct_line(level: int = 1) -> str:
    """Return the caller function or method line

    Args:
        level (int, optional): Index of previous caller. Defaults to 1.

    Returns:
        str: Caller function or method line
    """
    return inspect.stack()[level][__inspect_fct_line_index]


def get_current_fct_name(level: int = 1) -> str:
    """Return the caller function or method name

    Args:
        level (int, optional): Index of previous caller. Defaults to 1.

    Returns:
        str: Caller function or method name
    """
    return inspect.stack()[level][__inspect_fct_name_index]


def print_pos(level: int = 1):
    """Print the caller function or method name with filename and line

    Args:
        shift (int, optional): Shift level. Defaults to 0.
        suffix (str, optional): Suffix string. Defaults to ''.
        level (int, optional): Index of previous caller. Defaults to 1.
    """
    logger.debug(
        "Inspect: Function '%s' in file '%s', line %s\n" % (
            get_current_fct_name(level + 1),
            get_current_fct_filename(level + 1),
            get_current_fct_line(level + 1),
        )
    )
