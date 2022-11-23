https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
"""Assignment 2: DNA Manipulation"""

from typing import List
import palindromes


CYTOSINE = 'C'
GUANINE = 'G'
ADENINE = 'A'
THYMINE = 'T'


####### BEGIN PROVIDED HELPER FUNCTION ####################

def get_complementary_base(base: str) -> str:
    """Return the complement of base.

    Precondition: base in 'ATCG', base is not empty

    >>> get_complementary_base('A')
    'T'
    >>> get_complementary_base('C')
    'G'
    """

    if base == ADENINE:
        return THYMINE
    elif base == THYMINE:
        return ADENINE
    elif base == CYTOSINE:
        return GUANINE
    else:  # base == GUANINE
        return CYTOSINE


####### END PROVIDED HELPER FUNCTION ####################


# Delete these two lines and write your Task 2 code here.  Don't forget to
# run a2_simple_checker.py to check parameter and return types, and style!


if __name__ == '__main__':
    pass

    # Uncomment the next two lines to run the examples in your docstrings.
    #import doctest
    #doctest.testmod()
