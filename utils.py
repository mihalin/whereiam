from typing import List, Iterable, Any, Callable, Generator


def split_list(arg_list: Iterable[Any], predicate: Callable[[Any], bool]) -> Generator[List[Any], None, None]:
    """
    Slit list

    Example:
    split_list([True, False, False, True, False], lambda x: x) will be Generator
    ([True, False, False], [True, False])

    :param arg_list:
    :param predicate:
    :return:
    """
    current_list = []
    for element in arg_list:
        if predicate(element):
            if current_list:
                yield current_list
            current_list = []
        current_list.append(element)
    if current_list:
        yield current_list


if __name__ == '__main__':
    print([x for x in split_list([False, True, False, False, False, True, False, False, True, False], lambda x: x)])
