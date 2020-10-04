import math
from functools import reduce
from .decorators import empty_list, round_number


@empty_list
@round_number()
def best_time(times):
    """Returns the fastest time."""
    return min(map(lambda time: time.time, times))


@empty_list
@round_number()
def worst_time(times):
    """Returns the slowest time."""
    return max(map(lambda time: time.time, times))


@empty_list
@round_number()
def average_time(times):
    """Returns the average time of all included times."""
    times = list(map(lambda time: time.time, times))
    average = reduce(lambda acc, time: acc + time, times) / len(times)

    return average


@empty_list
@round_number()
def median_time(times):
    """Returns the median time of all included times."""
    times = list(map(lambda time: time.time, times))
    times.sort()
    mid = math.floor(len(times) / 2)
    median = times[mid] if len(times) % 2 else (times[mid - 1] + times[mid]) / 2

    return median
