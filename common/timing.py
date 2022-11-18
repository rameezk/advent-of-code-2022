from functools import wraps
import typing
import time


def timeit(f: typing.Callable):
    """Logs the execution time of a function"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        f()
        t2 = time.time()
        print(f"Execution time = {(t2 - t1) * 10**3} ms")

    return wrapper
