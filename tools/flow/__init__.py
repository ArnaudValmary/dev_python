#! /usr/bin/env python

import logging
from typing import Any, Callable, Dict, Final, Generator, List, Optional, Tuple, Union

from tools.inspect import get_fct_parameter_names

logger: logging.Logger = logging.getLogger('Flow')

final:     Final[bool] = True
not_final: Final[bool] = False


class FlowSkipData(Exception):
    """
    Exception raised when a function skips data.
    """
    pass


class FlowInitError(Exception):
    """
    Exception raised when init
    """
    pass


class FlowLoadError(Exception):
    """
    Exception raised when load
    """
    pass


class FlowFilterError(Exception):
    """
    Exception raised when filter
    """
    pass


class Flow:
    """
    A flow of data processing functions.

    The Flow class represents a series of data processing steps, where each step is a function that takes in some input data and produces output data.
    The flow is defined by a sequence of functions to apply, which are specified through the `fct_init`, `fct_load`, and `fct_filter` parameters.

    The Flow class provides a way to chain together these functions in a specific order, applying each one in turn to the input data.
    It also allows for filtering out certain inputs based on conditions specified by the filter functions.

    Attributes:
        fct_init (List[Callable]): A list of functions to initialize the flow with.
        fct_load (Callable): The function to load data from.
        fct_filter (List[Callable]): A list of filter functions to apply to the input data.
        context (Dict): The initial context for the flow.

    Methods:
        run(): Runs the flow and returns the final index and counts.
    """

    context_prefix: Final[str] = 'context:'

    def __add_flow_function_in_dict(self, fct: Callable) -> None:
        """
        Adds a function to the flow's dictionary, indicating whether its context is required.

        Args:
            fct (Callable): The function to add.
        """

        self.flow_functions_nb += 1
        if 'context' in get_fct_parameter_names(fct):
            self.flow_functions_dict[self.flow_functions_nb] = True
        else:
            self.flow_functions_dict[self.flow_functions_nb] = False

    def __add_modulo_function_in_dict(self, fct: Callable, modulo_n: int, idx_fct: int) -> None:
        """
        Adds or updates a modulo function in the dictionary based on whether it has a 'context' parameter.

        Args:
            fct (Callable): The function to check.
            modulo_n (int): The modulo value to store in the dictionary.
            idx_fct (int): The index of the function to store in the dictionary.
        """

        if 'context' in get_fct_parameter_names(fct):
            self.modulo_functions_dict[modulo_n, idx_fct] = True
        else:
            self.modulo_functions_dict[modulo_n, idx_fct] = False

    def __get_arg_integer_gt_zero(self, arg_value: Optional[Union[int, str]], comment: str) -> Optional[Union[int, str]]:
        """
        Validate and sanitize an argument value to ensure it meets good conditions.

        Checks if the provided `arg_value` is a valid integer greater than zero. If not,
        logs an error message and returns None.

        Additionally checks if the `arg_value` is a string that starts with the
        `context_prefix`. If not, logs another error message and returns None.

        Args:
            arg_value (Optional[Union[int, str]]): The value to be validated.
            comment (str): A human-readable description of the argument used for logging purposes.

        Returns:
            Optional[Union[int, str]]: The validated `arg_value` or None if it's invalid.
        """

        if arg_value is not None and isinstance(arg_value, int) and arg_value <= 0:
            logger.error("Flow: %s value is invalid integer: %d <= 0" % (comment, arg_value))
            arg_value = None
        if arg_value is not None and isinstance(arg_value, str) and not arg_value.startswith(self.context_prefix):
            logger.error("Flow: %s value is invalid str: '%s' doesn't starts by '%s'" % (comment, arg_value, self.context_prefix))
            arg_value = None
        return arg_value

    def __init__(self,
                 fct_init: Optional[Union[Callable, List[Callable]]] = None,
                 fct_load: Optional[Callable] = None,
                 fct_filter: Optional[Union[Callable, List[Callable]]] = None,
                 fct_finalyze: Optional[Union[Callable, List[Callable]]] = None,
                 fct_modulo: Optional[Dict[int, Union[Callable, List[Callable]]]] = None,
                 continue_if_none: bool = False,
                 ignore_last_filter_return: bool = True,
                 context: Optional[Dict] = None,
                 log_modulo: Optional[Union[int, str]] = None,
                 size_of_set: Optional[Union[int, str]] = None) -> None:
        """
        Initializes a new Flow instance.

        Args:
            fct_init(Union[Callable, List[Callable]]): The functions to initialize the flow.
            fct_load(Callable): The function to load data from .
            fct_filter(Union[Callable, List[Callable]]): The filters to apply to the data.
            fct_finalyze(Union[Callable, List[Callable]]): The final functions to apply after all filters on all data.
            continue_if_none(bool, optional): Whether to continue processing if a filter returns None. Defaults to False.
            ignore_last_filter_return(bool, optional): Whether to ignore the return value of the last filter. Defaults to True.
            context(Optional[Dict], optional): The initial context for the flow. Defaults to None.

        Raises:
            ValueError: If fct_init or fct_load are not callable.
        """

        self.flow_functions_dict: Dict[int, bool] = {}
        self.context: Dict = {}
        self.continue_if_none: bool = continue_if_none
        self.ignore_last_filter_return: bool = ignore_last_filter_return
        self.flow_functions_nb: int = 0
        self.flow_functions_final_start: int = 0
        self.modulo_functions_nb: int = 0
        self.modulo_functions_dict: Dict[int, Union[Callable, List[Callable]]] = {}
        self.size_of_set: Optional[Union[int, str]] = self.__get_arg_integer_gt_zero(size_of_set, 'size of set')
        self.log_modulo: Optional[Union[int, str]] = self.__get_arg_integer_gt_zero(log_modulo, 'log modulo')

        self.functions_init: List[Callable] = None
        if fct_init:
            if isinstance(fct_init, list):
                self.functions_init = fct_init
            else:
                self.functions_init = [fct_init]

        self.function_load: Callable = fct_load

        self.functions_filter: List[Callable] = None
        if fct_filter:
            if isinstance(fct_filter, list):
                self.functions_filter = fct_filter
            else:
                self.functions_filter = [fct_filter]

        self.functions_finalyze: List[Callable] = None
        if fct_finalyze:
            if isinstance(fct_finalyze, list):
                self.functions_finalyze = fct_finalyze
            else:
                self.functions_finalyze = [fct_finalyze]

        self.functions_modulo: Optional[Dict[int, Union[Callable, List[Callable]]]] = fct_modulo

        if context is not None:
            self.context = context

        logger.debug('Flow: init done')

    def __apply_filter_fct(self, data, fct_idx_tmp, fct) -> Any:
        """
        Applies a filter to the given data.

        Args:
            data(Any): The data to apply the filter to.
            fct_idx_tmp(int): The index of the filter.
            fct(Callable): The filter function.

        Returns:
            Any: The filtered data.
        """

        if self.flow_functions_dict[fct_idx_tmp]:
            data: Any = fct(data=data, context=self.context)
        else:
            data: Any = fct(data=data)

        return data

    def __apply_filters_fct(self, data, fct_idx_tmp) -> None:
        """
        Applies all filters to the given data.

        Args:
            data(Any): The data to apply the filters to.
            fct_idx_tmp(int): The index of the filter.
        """

        index: int = 0
        for index, fct in enumerate(self.functions_filter, start=1):
            fct_idx_tmp += 1
            data: Any = self.__apply_filter_fct(data, fct_idx_tmp, fct)
            if (data is None
                    and not self.continue_if_none
                    and
                    (
                        not self.ignore_last_filter_return
                        or index != self.nb_filters
                    )):
                self.nb_data_stopped_with_none += 1
                break
        else:
            self.nb_data_processed += 1

    def __build_function_dicts(self) -> None:
        """
        Builds the flow's dictionary with functions and their context requirements.
        """

        self.flow_functions_nb: int = 0

        if self.functions_init:
            for fct in self.functions_init:
                self.__add_flow_function_in_dict(fct)

        if self.function_load:
            self.__add_flow_function_in_dict(self.function_load)

        if self.functions_filter:
            for fct in self.functions_filter:
                self.__add_flow_function_in_dict(fct)

        if self.functions_finalyze:
            self.flow_functions_final_start = self.flow_functions_nb + 1
            for fct in self.functions_finalyze:
                self.__add_flow_function_in_dict(fct)

        if self.functions_modulo:
            new_functions_modulo: Dict[int, Union[Callable, List[Callable]]] = {}
            for modulo_n in self.functions_modulo:
                if modulo_n <= 0:
                    logger.error("Flow: modulo value is invalid integer: %d <= 0" % modulo_n)
                else:
                    modulos_fct: Union[Callable, List[Callable]] = self.functions_modulo[modulo_n]
                    if modulos_fct and not isinstance(modulos_fct, list):
                        modulos_fct = [modulos_fct]
                    if modulos_fct:
                        for idx_fct, fct in enumerate(modulos_fct, start=1):
                            self.__add_modulo_function_in_dict(fct, modulo_n, idx_fct)
                        new_functions_modulo[modulo_n] = modulos_fct
            if new_functions_modulo:
                self.functions_modulo = new_functions_modulo
            else:
                self.functions_modulo = None

    def __read_var_from_context_integer_gt_zero(self, fieldname: str, comment: Optional[str] = None) -> Optional[int]:
        """
        Retrieves an integer value from the context of a flow field.

        This method attempts to parse the provided `fieldname` as a string that
        represents an integer. If successful, it returns the parsed value; otherwise,
        it logs an error message and returns `None`.

        Args:
            fieldname (str): The name of the field in the context.
            comment (Optional[str], optional): A comment for logging purposes. Defaults to None.

        Returns:
            Optional[int]: The parsed integer value, or `None` if parsing fails.
        """

        value: Optional[Union[int, str]] = self.__getattribute__(fieldname)
        if comment is None:
            comment = fieldname.replace('_', ' ')
        if value is not None and isinstance(value, str):
            if value.startswith(self.context_prefix):
                value = value.replace(self.context_prefix, '', 1)
                if value in self.context:
                    value = self.context[value]
                    if value is not None:
                        if isinstance(value, int):
                            if value <= 0:
                                logger.error("Flow: %s value is invalid integer: %d <= 0" % (comment, value))
                                value = None
                        else:
                            logger.error("Flow: %s value is not an integer: %s" % (comment, value))
                            value = None
                else:
                    logger.error("Flow: %s value field name '%s' not in context" % (comment, value))
                    value = None
            else:
                logger.error("Flow: %s value is invalid str: '%s' doesn't starts by '%s'" % (comment, value, self.context_prefix))
                value = None
        return value

    def __init_vars(self) -> None:
        """
        Initializes instance variables from context values.

        This method reads two integer values from the context:
        - 'size_of_set': The number of elements in the set.
        - 'log_modulo': A modulo value used for logarithmic calculations.

        Both values are checked to ensure they are greater than zero, which is a valid input range.

        :param self: The instance of the class
        """

        self.size_of_set = self.__read_var_from_context_integer_gt_zero('size_of_set')
        self.log_modulo = self.__read_var_from_context_integer_gt_zero('log_modulo')

    def __init_flow(self, fct_idx: int = 0) -> int:
        """
        Initializes the flow and applies all functions.

        Args:
            fct_idx (int, optional): The index of the function to start with. Defaults to 0.

        Returns:
            int: The final index.
        """

        logger.debug("Flow: Init starts")

        for fct in self.functions_init:
            fct_idx += 1
            if self.flow_functions_dict[fct_idx]:
                fct(context=self.context)
            else:
                fct()

        self.__init_vars()

        logger.debug("Flow: Init ends")

        return fct_idx

    def __load_data(self, fct_idx: int = 0) -> Tuple[int, Generator]:
        """
        Loads data from the given function and applies all filters.

        Args:
            fct_idx (int, optional): The index of the function to start with. Defaults to 0.

        Returns:
            Tuple[int, Generator]: The final index and a generator of filtered data.
        """

        logger.debug("Flow: Call data generator")

        fct_idx += 1
        fct: Callable = self.function_load
        if self.flow_functions_dict[fct_idx]:
            all_data: Generator = fct(context=self.context)
        else:
            all_data: Generator = fct()

        logger.debug("Flow: End of call generator")

        return fct_idx, all_data

    def __apply_finalyze_fct(self, idx_fct, fct) -> None:
        """
        Applies the specified finalyze function.

        Args:
            idx_fct (int): The index of the function to be applied.
            fct (function): The function to be applied.
        """

        if self.flow_functions_dict[idx_fct]:
            fct(context=self.context)
        else:
            fct()

    def __apply_finalyzes_fct(self) -> None:
        """
        Applies all finalyze functions.
        """

        logger.debug("Flow: Finalyze starts")

        for idx_fct, fct in enumerate(self.functions_finalyze, start=self.flow_functions_final_start):
            self.__apply_finalyze_fct(idx_fct, fct)

        logger.debug("Flow: Finalyze ends")

    def __log_modulo(self, flag_final: bool = not_final) -> None:
        """
        Logs a message indicating the current state of the data set.

        If the size of the set is known (i.e., it has been initialized), logs the total number of data points and the percentage completion.
        Otherwise, logs only the total number of data points without any additional information.

        Args:
            flag_final (bool): A boolean indicating whether this is a final iteration or not. Defaults to False if not provided.
        """

        if self.size_of_set is None:
            logger.debug(
                "Flow: #data%s = %d" % (
                    ' (final)' if flag_final else '',
                    self.nb_data_total)
            )
        else:
            logger.debug(
                "Flow: #data%s = %d/%d (%3.2f%%)" % (
                    ' (final)' if flag_final else '',
                    self.nb_data_total,
                    self.size_of_set,
                    self.nb_data_total * 100 / self.size_of_set
                )
            )

    def __apply_modulo_fct(self, modulo_n, idx_fct, fct) -> None:
        """
        Applies the specified function to the data set with modulo functionality.

        If the specified index of function exists in the dictionary, applies it to the total number of data points with the given context.
        Otherwise, applies it to the total number of data points without any additional context.

        Args:
            modulo_n (int): The modulo number for which the function is applied.
            idx_fct (int): The index of the function to be applied.
            fct (function): The function to be applied to the data set.
        """

        if self.modulo_functions_dict[modulo_n, idx_fct]:
            fct(idx=self.nb_data_total, context=self.context)
        else:
            fct(idx=self.nb_data_total)

    def __apply_modulos_fct(self) -> None:
        """
        Applies all modulo functions to the data set based on its size and the given modulo numbers.

        Iterates through each modulo number and checks if the total number of data points is divisible by it.
        If it is, iterates through each function associated with that modulo number and applies them to the data set using the `__apply_modulo_fct` method.
        """

        for modulo_n in self.functions_modulo:
            if self.nb_data_total % modulo_n == 0:
                for idx_fct, fct in enumerate(self.functions_modulo[modulo_n], start=1):
                    self.__apply_modulo_fct(modulo_n, idx_fct, fct)

    def __filter_data(self, fct_idx: int, all_data: Generator) -> Tuple[int, int, int, int]:
        """
        Applies all filters to the given data.

        Args:
            fct_idx (int): The index of the function.
            all_data (Generator): A generator of unfiltered data.

        Returns:
            Tuple[int, int, int, int]: The total count, processed count, skipped count, and stopped by None count.
        """

        logger.debug("Flow: Apply filters")

        self.nb_filters: int = len(self.functions_filter)
        self.nb_data_total: int = 0
        self.nb_data_processed: int = 0
        self.nb_data_skip: int = 0
        self.nb_data_stopped_with_none: int = 0

        for data in all_data:
            self.nb_data_total += 1

            fct_idx_tmp: int = fct_idx
            try:
                self.__apply_filters_fct(data, fct_idx_tmp)
            except FlowSkipData as fsoe:
                self.nb_data_skip += 1
                logger.debug("FlowSkipData: %s" % fsoe)

            if self.functions_modulo:
                self.__apply_modulos_fct()

            if self.log_modulo and self.nb_data_total % self.log_modulo == 0:
                self.__log_modulo()

        if self.log_modulo:
            self.__log_modulo(final)

        logger.debug("Flow: End of filters")

        return self.nb_data_total, self.nb_data_processed, self.nb_data_skip, self.nb_data_stopped_with_none

    def run(self) -> Tuple[int, int, int, int]:
        """
        Runs the flow and returns the final index and counts.

        Returns:
            Tuple[int, int, int, int]: The final index, total count, processed count, and skipped count.
        """

        output_data: Tuple[int, int, int, int] = (0, 0, 0, 0)

        self.__build_function_dicts()

        fct_idx: int = 0
        if self.functions_init is None:
            logger.init("Flow: No init functions")
        else:
            fct_idx = self.__init_flow()

        if self.function_load is None:
            logger.warning("Flow: No load function")
        else:
            if self.functions_filter is None:
                logger.warning("Flow: No filter functions")
            else:
                all_data: Generator = None
                fct_idx, all_data = self.__load_data(fct_idx)
                output_data = self.__filter_data(fct_idx, all_data)

        if self.functions_finalyze is None:
            logger.info("Flow: No finalyze functions")
        else:
            self.__apply_finalyzes_fct()

        return output_data


#
# The lines below are for illustrative purposes only
#
if __name__ == '__main__':
    import os

    #
    # Configure logger
    #
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)  # Put logging.INFO to turn off Flow class logs

    #
    # Flow functions
    #
    def init_range_value(context: Dict) -> None:
        """
        Initializes a range value.

        Args:
            context (Dict): The initial context.
        """
        context['range_size'] = int(os.environ.get('range_size', 99))
        context['log_mod'] = 13
        context['nums'] = []
        logger.info("Init range_size to %d" % context['range_size'])

    def read_data_one_by_one(context) -> Generator[Dict[str, int], Any, None]:
        """
        Reads data one by one.

        Args:
            context (Dict): The initial context.

        Yields:
            Dict[str, int]: A dictionary of data.
        """
        logger.info("Read data...")
        for i in range(context['range_size']):
            logger.info("data internal integer is: %d" % i)
            yield {
                'num': i,
            }
        logger.info("...all data read data")

    def filter_even(data: Dict, context: Dict) -> Union[Dict, None]:
        """
        Filters even numbers.

        Args:
            data (Dict): The data to filter.
            context (Dict): The initial context.

        Returns:
            Union[Dict, None]: The filtered data or None if the number is not between 5 and 8.
        """
        if (data.get('num', None) > 5 and data.get('num', None) < 20) or data.get('num', None) % 5 == 0:
            raise FlowSkipData('Ignore this num %d' % data.get('num', None))
        if data.get('num', None) % 2 == 0:
            return data

    def print_data(data: Dict) -> None:
        """
        Prints the data.

        Args:
            data (Dict): The data to print.
        """
        logger.info("data is: %s" % data)
        cur_context['nums'].append(data.get('num', None))

    def call_48(idx: int) -> None:
        logger.info("CALL_48:%d" % idx)

    def call_49(idx: int, context: Dict) -> None:
        logger.info("CALL_49:%d (%s)" % (idx, context))

    def call_49BIS(idx: int) -> None:
        logger.info("CALL_49BIS:%d" % (idx))

    def finalyze_1() -> None:
        logger.info('Finalyze 1')

    def finalyze_2(context: Dict) -> None:
        logger.info('Finalyze 2, context=%s' % context)

    #
    # Run flow
    #
    cur_nb_data_total: int = 0
    cur_nb_data_processed: int = 0
    cur_nb_data_skip: int = 0
    cur_nb_data_stopped_by_none: int = 0
    cur_size_of_set: int = 99
    cur_context: Dict = {}
    (cur_nb_data_total, cur_nb_data_processed, cur_nb_data_skip, cur_nb_data_stopped_by_none) = Flow(
        fct_init=[
            init_range_value,
        ],
        fct_load=read_data_one_by_one,
        fct_filter=[
            filter_even,
            print_data,
        ],
        fct_finalyze=[
            finalyze_1,
            finalyze_2,
        ],
        continue_if_none=False,
        context=cur_context,
        log_modulo='context:log_mod',
        size_of_set='context:range_size',
        fct_modulo={
            48: call_48,
            49: [call_49, call_49BIS],
        }
    ).run()

    logger.info("End of flow")
    logger.info("context is: %s" % cur_context)

    if cur_nb_data_total > 0:
        logger.info(
            "nb_data_all=%d / nb_data_ok=%d (%3.2f%%) / self.nb_data_skip=%d (%3.2f%%) / nb_data_none=%d (%3.2f%%)" %
            (
                cur_nb_data_total,
                cur_nb_data_processed,
                cur_nb_data_processed * 100 / cur_nb_data_total,
                cur_nb_data_skip,
                cur_nb_data_skip * 100 / cur_nb_data_total,
                cur_nb_data_stopped_by_none,
                cur_nb_data_stopped_by_none * 100 / cur_nb_data_total
            )
        )
    else:
        logger.info("no data")
