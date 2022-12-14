https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis-python
#
# Most of this work is copyright (C) 2013-2018 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import division, print_function, absolute_import

import math

import hypothesis.internal.conjecture.utils as d
import hypothesis.internal.conjecture.floats as flt
from hypothesis.control import assume
from hypothesis.internal.floats import sign
from hypothesis.internal.conjecture.utils import calc_label_from_name
from hypothesis.searchstrategy.strategies import SearchStrategy


class IntStrategy(SearchStrategy):
    """A generic strategy for integer types that provides the basic methods
    other than produce.

    Subclasses should provide the produce method.
    """


class IntegersFromStrategy(SearchStrategy):

    def __init__(self, lower_bound, average_size=100000.0):
        super(IntegersFromStrategy, self).__init__()
        self.lower_bound = lower_bound
        self.average_size = average_size

    def __repr__(self):
        return 'IntegersFromStrategy(%d)' % (self.lower_bound,)

    def do_draw(self, data):
        return int(
            self.lower_bound + d.geometric(data, 1.0 / self.average_size))


class WideRangeIntStrategy(IntStrategy):

    distribution = d.Sampler([
        4.0, 8.0, 1.0, 1.0, 0.5
    ])

    sizes = [8, 16, 32, 64, 128]

    def __repr__(self):
        return 'WideRangeIntStrategy()'

    def do_draw(self, data):
        size = self.sizes[self.distribution.sample(data)]
        r = data.draw_bits(size)
        sign = r & 1
        r >>= 1
        if sign:
            r = -r
        return int(r)


class BoundedIntStrategy(SearchStrategy):
    """A strategy for providing integers in some interval with inclusive
    endpoints."""

    def __init__(self, start, end):
        SearchStrategy.__init__(self)
        self.start = start
        self.end = end

    def __repr__(self):
        return 'BoundedIntStrategy(%d, %d)' % (self.start, self.end)

    def do_draw(self, data):
        return d.integer_range(data, self.start, self.end)


NASTY_FLOATS = sorted([
    0.0, 0.5, 1.1, 1.5, 1.9, 1.0 / 3, 10e6, 10e-6, 1.175494351e-38,
    2.2250738585072014e-308,
    1.7976931348623157e+308, 3.402823466e+38, 9007199254740992, 1 - 10e-6,
    2 + 10e-6, 1.192092896e-07, 2.2204460492503131e-016,

] + [float('inf'), float('nan')] * 5, key=flt.float_to_lex)
NASTY_FLOATS = list(map(float, NASTY_FLOATS))
NASTY_FLOATS.extend([-x for x in NASTY_FLOATS])

FLOAT_STRATEGY_DO_DRAW_LABEL = calc_label_from_name(
    'getting another float in FloatStrategy')


class FloatStrategy(SearchStrategy):
    """Generic superclass for strategies which produce floats."""

    def __init__(self, allow_infinity, allow_nan):
        SearchStrategy.__init__(self)
        assert isinstance(allow_infinity, bool)
        assert isinstance(allow_nan, bool)
        self.allow_infinity = allow_infinity
        self.allow_nan = allow_nan

        self.nasty_floats = [f for f in NASTY_FLOATS if self.permitted(f)]
        weights = [
            0.2 * len(self.nasty_floats)
        ] + [0.8] * len(self.nasty_floats)
        self.sampler = d.Sampler(weights)

    def __repr__(self):
        return '%s()' % (self.__class__.__name__,)

    def permitted(self, f):
        assert isinstance(f, float)
        if not self.allow_infinity and math.isinf(f):
            return False
        if not self.allow_nan and math.isnan(f):
            return False
        return True

    def do_draw(self, data):
        while True:
            data.start_example(FLOAT_STRATEGY_DO_DRAW_LABEL)
            i = self.sampler.sample(data)
            if i == 0:
                result = flt.draw_float(data)
            else:
                result = self.nasty_floats[i - 1]
                flt.write_float(data, result)
            data.stop_example()
            if self.permitted(result):
                return result


def float_order_key(k):
    return (sign(k), k)


class FixedBoundedFloatStrategy(SearchStrategy):
    """A strategy for floats distributed between two endpoints.

    The conditional distribution tries to produce values clustered
    closer to one of the ends.
    """

    def __init__(self, lower_bound, upper_bound):
        SearchStrategy.__init__(self)
        self.lower_bound = float(lower_bound)
        self.upper_bound = float(upper_bound)
        assert not math.isinf(self.upper_bound - self.lower_bound)
        lb = float_order_key(self.lower_bound)
        ub = float_order_key(self.upper_bound)

        self.critical = [
            z for z in (-0.0, 0.0)
            if lb <= float_order_key(z) <= ub
        ]
        self.critical.append(self.lower_bound)
        self.critical.append(self.upper_bound)

    def __repr__(self):
        return 'FixedBoundedFloatStrategy(%s, %s)' % (
            self.lower_bound, self.upper_bound,
        )

    def do_draw(self, data):
        f = self.lower_bound + (
            self.upper_bound - self.lower_bound) * d.fractional_float(data)
        assume(self.lower_bound <= f <= self.upper_bound)
        assume(sign(self.lower_bound) <= sign(f) <= sign(self.upper_bound))
        # Special handling for bounds of -0.0
        for g in [self.lower_bound, self.upper_bound]:
            if f == g:
                f = math.copysign(f, g)
        return f
