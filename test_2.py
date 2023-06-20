import os
import datetime
from functools import wraps


def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            start = datetime.datetime.now()
            result = old_function(*args, **kwargs)
            end = datetime.datetime.now()

            with open(path, 'a') as log_file:
                log_file.write(f"{start} - Called function: {old_function.__name__}\n")
                log_file.write(f"Arguments: {args}, {kwargs}\n")
                log_file.write(f"Returned value: {result}\n")
                log_file.write(f"Execution time: {end - start}\n\n")

            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:
        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'
#дз № 3
class FlatIterator:

    @logger('flat_iterator.log')
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.count_index = 0
        self.count_item = 0

    @logger('flat_iterator.log')
    def __iter__(self):
        return self

    @logger('flat_iterator.log')
    def __next__(self):
        if self.count_index >= len(self.list_of_list):
            raise StopIteration

        current_list = self.list_of_list[self.count_index]

        if self.count_item >= len(current_list):
            self.count_index += 1
            self.count_item = 0
            return self.__next__()
        item = current_list[self.count_item]
        self.count_item += 1
        return item


def test_flat_iterator():
    nested_list = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    flat_iter = FlatIterator(nested_list)

    result = []
    for item in flat_iter:
        result.append(item)

    assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9], "The flattened list should be [1, 2, 3, 4, 5, 6, 7, 8, 9]"


if __name__ == '__main__':
    test_2()
    test_flat_iterator()