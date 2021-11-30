import itertools
from typing import Iterable, Optional, Tuple


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


def sofa_find_candidate(bits: list[int], sofa_upper_limit: int, max_num: int) -> Optional[Tuple[int, list[int]]]:
    """
    check a set (=row/column/square) for the number with fewest possible empty cell position.
    related to the concept of 'set-oriented freedom analysis' and 'hidden single' technique

    >>> set = [-5, -3, -4, 223, 223, -8, 445, -1, 447]
    >>> sofa_find_candidate(set, 3, 9)
    (2, [6])
    >>> set2 = [287, 446, 286, 474, 450, -2, 303, -9, 303]
    >>> sofa_find_candidate(set2, 3, 9)
    (4, [4])
    >>> set3 = [125, 252, 380, 250, 234, -7, -6, 489, -4]
    >>> sofa_find_candidate(set3, 3, 9)
    (5, [4, 7])
    >>> set4 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> print(sofa_find_candidate(set4, 3, 9))
    None
    >>> set5 = [63, 63, 63, -1, -2, -3, -4, -5, -6]
    >>> print(sofa_find_candidate(set5, 3, 9))
    None
    >>> set6 = [63, 63, 127, -1, -2, -3, -4, -5, -6]
    >>> print(sofa_find_candidate(set6, 3, 9))
    (7, [0, 1])
    """
    result = None
    for i in range(1, max_num + 1):  # traverse each sudoku numbers
        check_bit = 1 << (i - 1)
        seen = []
        for (pos, bit) in enumerate(bits):
            if bit < 0:  # bypass the negative bits, which represent occupied cells
                continue
            if bit & check_bit == 0:  # number i is valid for that cell
                seen.append(pos)
            if len(seen) >= sofa_upper_limit:
                break
        if seen and len(seen) < sofa_upper_limit:
            result = (i, seen)
            sofa_upper_limit = len(seen)
        if seen == 1:  # return early if a number got only 1 free cell available
            return result

    return result
