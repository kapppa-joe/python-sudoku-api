BitTable = {}


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
