https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
""" This should not warn about `prop` being abstract in Child """
# pylint: disable=too-few-public-methods, no-absolute-import,metaclass-assignment, useless-object-inheritance

import abc

class Parent(object):
    """Abstract Base Class """
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def prop(self):
        """ Abstract """

class Child(Parent):
    """ No warning for the following. """
    prop = property(lambda self: 1)
