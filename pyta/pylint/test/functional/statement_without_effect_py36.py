https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
"""Test for statements without effects."""
# pylint: disable=too-few-public-methods, useless-object-inheritance


class ClassLevelAttributeTest(object):
    """ test attribute docstrings. """

    some_variable: int = 42
    """Data docstring"""

    some_other_variable: int = 42
    """Data docstring"""

    def func(self):
        """Some Empty Docstring"""

    # +1: [pointless-string-statement]
    """useless"""
