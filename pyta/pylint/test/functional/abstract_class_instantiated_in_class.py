https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
"""Don't warn if the class is instantiated in its own body."""
# pylint: disable=missing-docstring, useless-object-inheritance


import abc

import six


@six.add_metaclass(abc.ABCMeta)
class Ala(object):

    @abc.abstractmethod
    def bala(self):
        pass

    @classmethod
    def portocala(cls):
        instance = cls()
        return instance
