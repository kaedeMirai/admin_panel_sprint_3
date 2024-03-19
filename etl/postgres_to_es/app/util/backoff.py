import time
from functools import wraps

import logging
logging.getLogger().setLevel(logging.INFO)


def backoff(exceptions: tuple, start_sleep_time: float = 0.1, factor: int = 2, border_sleep_time: int = 10,
            max_amount_of_calls: int = 50):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * (factor ^ n), если t < border_sleep_time
        t = border_sleep_time, иначе
    :param exceptions: ошибки, которы будет ловить функция
    :param start_sleep_time: начальное время ожидания
    :param factor: во сколько раз нужно увеличивать время ожидания на каждой итерации
    :param border_sleep_time: максимальное время ожидания
    :param max_amount_of_calls: максимальное количество попыток подключения
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            for i in range(max_amount_of_calls):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logging.error(str(e))
                    logging.info(f'Trying to reconnect...')

                    time_to_sleep = start_sleep_time * (factor ** i)
                    if time_to_sleep > border_sleep_time:
                        time_to_sleep = border_sleep_time

                    time.sleep(time_to_sleep)

        return inner

    return func_wrapper
