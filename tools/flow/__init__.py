#! /usr/bin/env python

import inspect
import logging
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

logger: logging.Logger = logging.getLogger('Flow')

#
# Function who could be moved in another file
#


def get_fct_parameter_names(fct: Callable) -> List[str]:
    """
    Returns the list of parameter names from the given function.

    Args:
        fct (Callable): The function to extract parameters from.

    Returns:
        List[str]: The list of parameter names.
    """
    return list(inspect.signature(fct).parameters.keys())

#
# Flow classes
#


class FlowSkipData(Exception):
    """
    Exception raised when a function skips data.
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

    def __add_function_in_dict(self, fct: Callable) -> None:
        """
        Adds a function to the flow's dictionary, indicating whether its context is required.

        Args:
            fct (Callable): The function to add.
        """
        self.functions_nb += 1
        if 'context' in get_fct_parameter_names(fct):
            self.functions_dict[self.functions_nb] = True
        else:
            self.functions_dict[self.functions_nb] = False

    def __init__(self,
                 fct_init: Union[Callable, List[Callable]],
                 fct_load: Callable,
                 fct_filter: Union[Callable, List[Callable]],
                 continue_if_none: bool = False,
                 ignore_last_filter_return: bool = True,
                 context: Optional[Dict] = None) -> None:
        """
        Initializes a new Flow instance.

        Args:
            fct_init (Union[Callable, List[Callable]]): The functions to initialize the flow.
            fct_load (Callable): The function to load data from.
            fct_filter (Union[Callable, List[Callable]]): The filters to apply to the data.
            continue_if_none (bool, optional): Whether to continue processing if a filter returns None. Defaults to False.
            ignore_last_filter_return (bool, optional): Whether to ignore the return value of the last filter. Defaults to True.
            context (Optional[Dict], optional): The initial context for the flow. Defaults to None.

        Raises:
            ValueError: If fct_init or fct_load are not callable.
        """
        self.functions_dict: Dict[int, bool] = {}
        self.context: Dict = {}
        self.continue_if_none: bool = continue_if_none
        self.ignore_last_filter_return: bool = ignore_last_filter_return
        self.functions_nb: int = 0

        self.functions_init: List[Callable] = None
        if not isinstance(fct_init, list):
            self.functions_init = [fct_init]
        else:
            self.functions_init = fct_init

        self.function_load: Callable = fct_load

        self.functions_filter: List[Callable] = None
        if not isinstance(fct_init, list):
            self.functions_filter = [fct_filter]
        else:
            self.functions_filter = fct_filter

        if context is not None:
            self.context = context

        logger.debug('Flow init done')

    def __apply_filter(self, data, fct_idx_tmp, fct) -> Any:
        """
        Applies a filter to the given data.

        Args:
            data (Any): The data to apply the filter to.
            fct_idx_tmp (int): The index of the filter.
            fct (Callable): The filter function.

        Returns:
            Any: The filtered data.
        """
        if self.functions_dict[fct_idx_tmp]:
            data: Any = fct(data=data, context=self.context)
        else:
            data: Any = fct(data=data)
        return data

    def __apply_filters(self, data, fct_idx_tmp) -> None:
        """
        Applies all filters to the given data.

        Args:
            data (Any): The data to apply the filters to.
            fct_idx_tmp (int): The index of the filter.
        """
        index: int = 0
        for index, fct in enumerate(self.functions_filter, start=1):
            fct_idx_tmp += 1
            data: Any = self.__apply_filter(data, fct_idx_tmp, fct)
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

    def __build_function_dict(self) -> None:
        """
        Builds the flow's dictionary with functions and their context requirements.
        """
        self.functions_nb: int = 0

        for fct in self.functions_init:
            self.__add_function_in_dict(fct)

        self.__add_function_in_dict(self.function_load)

        for fct in self.functions_filter:
            self.__add_function_in_dict(fct)

    def __init_flow(self, fct_idx: int = 0) -> int:
        """
        Initializes the flow and applies all functions.

        Args:
            fct_idx (int, optional): The index of the function to start with. Defaults to 0.

        Returns:
            int: The final index.
        """
        logger.debug("Init...")
        for fct in self.functions_init:
            fct_idx += 1
            if self.functions_dict[fct_idx]:
                fct(context=self.context)
            else:
                fct()
        logger.debug("...end of init")
        return fct_idx

    def __load_data(self, fct_idx: int = 0) -> Tuple[int, Generator]:
        """
        Loads data from the given function and applies all filters.

        Args:
            fct_idx (int, optional): The index of the function to start with. Defaults to 0.

        Returns:
            Tuple[int, Generator]: The final index and a generator of filtered data.
        """
        logger.debug("Call data generator...")
        fct_idx += 1
        fct: Callable = self.function_load
        if self.functions_dict[fct_idx]:
            all_data: Generator = fct(context=self.context)
        else:
            all_data: Generator = fct()
        logger.debug("End of call generator")
        return fct_idx, all_data

    def __filter_data(self, fct_idx: int, all_data: Generator) -> Tuple[int, int, int, int]:
        """
        Applies all filters to the given data.

        Args:
            fct_idx (int): The index of the function.
            all_data (Generator): A generator of unfiltered data.

        Returns:
            Tuple[int, int, int, int]: The total count, processed count, skipped count, and stopped by None count.
        """
        logger.debug("Apply filters...")
        self.nb_filters: int = len(self.functions_filter)
        self.nb_data_total: int = 0
        self.nb_data_processed: int = 0
        self.nb_data_skip: int = 0
        self.nb_data_stopped_with_none: int = 0
        for data in all_data:
            self.nb_data_total += 1
            fct_idx_tmp: int = fct_idx
            try:
                self.__apply_filters(data, fct_idx_tmp)
            except FlowSkipData as fsoe:
                self.nb_data_skip += 1
                logger.debug("FlowSkipData: %s" % fsoe)
        logger.debug("...end of filters")
        return self.nb_data_total, self.nb_data_processed, self.nb_data_skip, self.nb_data_stopped_with_none

    def run(self) -> Tuple[int, int, int, int]:
        """
        Runs the flow and returns the final index and counts.

        Returns:
            Tuple[int, int, int, int]: The final index, total count, processed count, and skipped count.
        """
        self.__build_function_dict()

        fct_idx: int = self.__init_flow()
        fct_idx, all_data = self.__load_data(fct_idx)
        return self.__filter_data(fct_idx, all_data)


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
        context['range_size'] = int(os.environ.get('range_size', 10))
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
        if data.get('num', None) > 5 and data.get('num', None) < 8:
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
        context['nums'].append(data.get('num', None))

    #
    # Run flow
    #
    nb_data_total: int = 0
    nb_data_processed: int = 0
    nb_data_skip: int = 0
    nb_data_stopped_by_none: int = 0
    context: Dict = {}
    (nb_data_total, nb_data_processed, nb_data_skip, nb_data_stopped_by_none) = Flow(
        fct_init=[
            init_range_value,
        ],
        fct_load=read_data_one_by_one,
        fct_filter=[
            filter_even,
            print_data,
        ],
        continue_if_none=False,
        context=context
    ).run()

    logger.info("End of flow")
    logger.info("context is: %s" % context)

    if nb_data_total > 0:
        logger.info(
            "nb_data_all=%d / nb_data_ok=%d (%3.2f%%) / self.nb_data_skip=%d (%3.2f%%) / nb_data_none=%d (%3.2f%%)" %
            (
                nb_data_total,
                nb_data_processed,
                nb_data_processed * 100 / nb_data_total,
                nb_data_skip,
                nb_data_skip * 100 / nb_data_total,
                nb_data_stopped_by_none,
                nb_data_stopped_by_none * 100 / nb_data_total
            )
        )
    else:
        logger.info("no data")
