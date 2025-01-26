"""
Wrapper functions to measure function's performance.
"""

import time

from app.common.utils.utils import datetime_now_sec


def measure_execution_time(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(
                f"[{datetime_now_sec()}] function {func.__name__} took {execution_time:.4f} seconds to execute"
            )
            return result

        return wrapper

    return decorator
