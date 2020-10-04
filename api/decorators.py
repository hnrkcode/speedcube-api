import functools


def round_number(decimals=0):
    """Round the number to a certain number of decimals."""

    def decorator_round_number(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not decimals:
                return int(round(func(*args, **kwargs), decimals))
            return round(func(*args, **kwargs), decimals)

        return wrapper

    return decorator_round_number


def empty_list(func):
    """Returns 0 because an empty list means there are no saved times."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        times = len(args[0])
        if not times:
            return 0
        return func(*args, **kwargs)

    return wrapper
