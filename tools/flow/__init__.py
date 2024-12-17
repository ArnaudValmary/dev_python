#! /usr/bin/env python

import inspect
import logging
import os
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

logger: logging.Logger = logging.getLogger('Flow')


class FlowSkipData(Exception):
    pass


class Flow:

    def add_function_in_dict(self, fct: Callable) -> None:
        self.functions_nb += 1
        if 'context' in inspect.signature(fct).parameters:
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
        if self.functions_dict[fct_idx_tmp]:
            data: Any = fct(data=data, context=self.context)
        else:
            data: Any = fct(data=data)
        return data

    def __apply_filters(self, data, fct_idx_tmp) -> None:
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

    def run(self) -> Tuple[int, int, int, int]:

        # Determine if 'context' is in functions parameters
        self.functions_nb: int = 0

        for fct in self.functions_init:
            self.add_function_in_dict(fct)

        self.add_function_in_dict(self.function_load)

        for fct in self.functions_filter:
            self.add_function_in_dict(fct)

        fct_idx: int = 0

        # Init
        logger.debug("Init...")
        for fct in self.functions_init:
            fct_idx += 1
            if self.functions_dict[fct_idx]:
                fct(context=self.context)
            else:
                fct()
        logger.debug("...end of init")

        # Data loading
        logger.debug("Call data generator...")
        fct_idx += 1
        fct: Callable = self.function_load
        if self.functions_dict[fct_idx]:
            all_data: Generator = fct(context=self.context)
        else:
            all_data: Generator = fct()
        logger.debug("End of call generator")

        # Run flow
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

        return (self.nb_data_total, self.nb_data_processed, self.nb_data_skip, self.nb_data_stopped_with_none)


if __name__ == '__main__':
    def init_range_value(context: Dict) -> None:
        context['range_size'] = int(os.environ.get('range_size', 10))
        context['nums'] = []
        print("Init range_size to %d" % context['range_size'])

    def read_data_one_by_one(context) -> Generator[Dict[str, int], Any, None]:
        print("Read data...")
        for i in range(context['range_size']):
            print("n=%d" % i)
            yield {
                'num': i,
            }

    def filter_even(data: Dict, context: Dict) -> Union[Dict, None]:
        if data.get('num', None) > 5 and data.get('num', None) < 8:
            raise FlowSkipData('Ignore this num %d' % data.get('num', None))
        if data.get('num', None) % 2 == 0:
            return data

    def print_data(data: Dict) -> None:
        print(data)
        context['nums'].append(data.get('num', None))

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    nb_data_total: int = 0
    nb_data_processed: int = 0
    nb_data_skip: int = 0
    nb_data_stopped_by_none: int = 0
    context: Dict = {}
    (nb_data_total, nb_data_processed, nb_data_skip, nb_data_stopped_by_none) = flow = Flow(
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

    print("context=%s" % context)

    if nb_data_total > 0:
        print(
            "nb_data_ok=%d / self.nb_data_skip=%d / nb_data_all=%d (%3.2f%%) / nb_data_none=%d" %
            (
                nb_data_processed,
                nb_data_skip,
                nb_data_total,
                nb_data_processed * 100 / nb_data_total,
                nb_data_stopped_by_none
            )
        )
    else:
        print("no data")
