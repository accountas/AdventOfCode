import random
from time import perf_counter
from common.data import *
from functools import cache

import sys

sys.set_int_max_str_digits(10**6)


def arithmetic_sum(start, end):
    n = end - start + 1
    return n * (start + end) // 2


def geometric_sum(start, ratio, n):
    if n <= 0:
        return 0
    if ratio == 1:
        return start * n
    return start * (ratio**n - 1) // (ratio - 1)


def divisors(n):
    for i in range(1, n + 1):
        if n % i == 0:
            yield i


@cache
def F(limit: int, period_length: int, repetitions: int):
    """
    Calculates the sum of numbers <= `limit` that are formed by repeating any
    base pattern of length `period_length` exactly `repetitions` times.

    Only considers numbers that have minimal period of length `period_length`
    E.g. 12121212 is periodic by 4, but is not included when period_length=4 as its minimal period length is 2.
    """

    # Step 1: Find the maximum valid base
    # We need to find the largest base pattern (e.g., 123) such that
    # repeating it `repetitions` times stays within the `limit`.
    limit_str = str(limit)
    min_possible = int(
        str(10 ** (period_length - 1)) * repetitions
    )  # 100..0100..0100..0

    if limit < min_possible:
        return 0

    if len(limit_str) > period_length * repetitions:
        # 9999.. all periods work, each number is simply shorter than the limit
        max_base = 10**period_length - 1
    else:
        # The base cannot exceed the first `period_length` digits of the limit.
        prefix = limit_str[:period_length]
        max_base = int(prefix)

        # Sometimes it's too much, decrease
        if prefix * repetitions > limit_str:
            max_base -= 1

    # Step 2: Calculate the sum of all periods from 10^(period_length-1) to max_base
    # A periodic number can be expressed as: base * factor.
    #    Example: (period=3, reps=3):
    #      100100100 = 100 * 1001001
    #      101101101 = 101 * 1001001
    #      ...
    #      123123123 = 123 * 1001001
    #      ...
    #      ___
    #      AAA       = A   * 1001001 (A = max_base)
    #      The sum can be simplified to SUM(valid bases) * factor.
    factor = geometric_sum(1, 10**period_length, repetitions)
    period_sum = arithmetic_sum(10 ** (period_length - 1), max_base)

    # Step 3: Remove contributions of already periodic base patterns
    # `period_sum` currently includes bases that are themselves periodic (e.g. '1212').
    # Subtract them to ensure the *minimal* period constraint is satisfied.
    #
    # Example: Processing F(limit=12340000, period=4, reps=2).
    #  max_base calculated in Step 1 is 1233.
    #    We have summed [1000..1233], but need to remove:
    #      - Sum of period 2 bases: 1010, 1212... (Calculated by F(1233, 2, 2))
    #      - Sum of period 1 bases: 1111...       (Calculated by F(1233, 1, 4))
    #
    # Proof this works is left as an exercise to the reader. But in summary this relies on
    # two key properties:
    # - Every number/sequence has exactly one minimal period
    #   => Every call to F here considers a disjoint set of numbers
    # - Every valid period length is a multiple of minimal period length
    #   => If repeating base pattern forms a number that has a shorter period than the pattern itself
    #      It means the pattern is also periodic
    #   * TBH it's "proof by intuition" but this https://en.wikipedia.org/wiki/Fine_and_Wilf%27s_theorem
    #     looks like something that can be used to show this
    for div in divisors(period_length):
        if div != period_length:
            period_sum -= F(max_base, div, period_length // div)

    # Step 4: Profit
    return period_sum * factor


def bad_id_sum(limit: int, filter=None):
    """
    Compute the sum of numbers <= limit that are periodic

    Idea:
    All periodic numbers can be grouped into buckets by their length and minimal period.
    Each number lands in exactly one bucket.
    We have a function F to compute the sum of all numbers from a given bucket.
    => Iterate all possible buckets and sum their sizes
    """
    num_digits = len(str(limit))

    total = 0
    for period in range(1, num_digits // 2 + 1):
        max_repetitions = num_digits // period

        for rep in range(2, max_repetitions + 1):
            if filter is None or filter(rep, period):
                total += F(limit, period, rep)

    return total


def bad_id_sum_for_range(l: int, r: int, filter=None):
    return bad_id_sum(r, filter) - bad_id_sum(l - 1, filter)


def main():
    ranges = [
        list(map(int, r.split("-")))
        for r in get_data(year=2025, day=2, sample=True).split(",")
    ]

    part1 = 0
    part2 = 0

    for l, r in ranges:
        part1 += bad_id_sum_for_range(l, r, lambda reps, _: reps % 2 == 0)
        part2 += bad_id_sum_for_range(l, r)

    print("Part 1:", part1)
    print("Part 2:", part2)
    print("[1 to Googol]: ", bad_id_sum_for_range(1, 10**100))


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    duration_ms = (end_time - start_time) * 1000
    print(f"Duration: {duration_ms:.2f} ms")
