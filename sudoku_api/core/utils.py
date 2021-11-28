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


LookupTable = {}


def conv_bit_to_num_list(input: int):
    """
    convert bit notation to a list of numbers
    >>> conv_bit_to_num_list(0)
    []
    >>> conv_bit_to_num_list(3)
    [1, 2]
    >>> conv_bit_to_num_list(79)
    [1, 2, 3, 4, 7]
    """
    if input in LookupTable:
        return LookupTable[input]
    nums = []
    count = 1
    bit = input
    while bit != 0:
        if bit & 1:
            nums.append(count)
        count += 1
        bit >>= 1
    LookupTable[input] = nums
    return nums


def replace_string(string: str, idx: int, char: str) -> str:
    """
    replace the nth char in a string
    >>> replace_string('star', 1, 'p')
    'spar'
    >>> replace_string('cattle', 0, 'b')
    'battle'
    >>> replace_string('list', 3, 'p')
    'lisp'
    >>> replace_string('python', 10, 'rabbit')
    'python'
    >>> replace_string('ruby', -3, 'perl')
    'ruby'
    """
    if idx < 0 or idx > len(string):
        return string
    if len(char) > 1:
        char = char[0]
    return string[0:idx] + char + string[idx+1:len(string)]
