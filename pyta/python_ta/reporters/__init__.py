https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
from .color_reporter import ColorReporter
from .html_reporter import HTMLReporter
from .plain_reporter import PlainReporter
from .stat_reporter import StatReporter
from .position_reporter import PositionReporter

# Export tuple of reporter classes for python_ta init file.
REPORTERS = (ColorReporter, PlainReporter, HTMLReporter, StatReporter, PositionReporter)
