from typing import Iterable
import itertools


BitTable = {}


def all_unique(iter: Iterable) -> bool:
    """ util function to check whether every element in iterable is unique
    >>> all_unique('abcd')
    True
    >>> all_unique('apple')
    False
    >>> all_unique([1,2,3,4,5,6,7,8,9])
    True
    >>> all_unique([1,2,3,1,5,6,7,8,9])
    False

    Should return early.
    >>> all_unique(itertools.chain(range(5), itertools.repeat(1)))
    False
    """
    seen = set()
    return not any(elem in seen or seen.add(elem) for elem in iter)


def count_bit(num: int) -> int:
    """ util function to count the 1 bits in a binary number
    >>> count_bit(0)
    0

    >>> count_bit(1)
    1

    >>> count_bit(8)
    1

    >>> count_bit(3)
    2

    >>> count_bit(500)
    6
    """
    if num in BitTable:
        return BitTable[num]
    else:
        count = 0
        bit = num
        while bit != 0:
            count += 1
            bit = bit & (bit - 1)
        BitTable[num] = count
        return count
