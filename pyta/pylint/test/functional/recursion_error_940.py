https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
# pylint: disable=missing-docstring, too-few-public-methods, useless-object-inheritance
import datetime


class NewDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(2010, 1, 1)


class Next(object):
    def __init__(self):
        datetime.date = NewDate
