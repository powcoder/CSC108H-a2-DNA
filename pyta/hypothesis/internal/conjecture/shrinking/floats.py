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

import sys
import math

from hypothesis.internal.conjecture.floats import float_to_lex
from hypothesis.internal.conjecture.shrinking.common import Shrinker
from hypothesis.internal.conjecture.shrinking.integer import Integer

MAX_PRECISE_INTEGER = 2 ** 53


class Float(Shrinker):

    def setup(self):
        self.NAN = float('nan')
        self.debugging_enabled = True

    def make_immutable(self, f):
        f = float(f)
        if math.isnan(f):
            # Always use the same NAN so it works properly in self.seen
            f = self.NAN
        return f

    def check_invariants(self, value):
        # We only handle positive floats because we encode the sign separately
        # anyway.
        assert not (value < 0)

    def left_is_better(self, left, right):
        lex1 = float_to_lex(left)
        lex2 = float_to_lex(right)
        return lex1 < lex2

    def short_circuit(self):
        for g in [sys.float_info.max, float('inf'), float('nan'), ]:
            self.consider(g)

        # If we're stuck at a nasty float don't try to shrink it further. These
        if math.isinf(self.current) or math.isnan(self.current):
            return True

        # If its too large to represent as an integer, bail out here. It's
        # better to try shrinking it in the main representation.
        return self.current >= MAX_PRECISE_INTEGER

    def run_step(self):
        # We check for a bunch of standard "large" floats. If we're currently
        # worse than them and the shrink downwards doesn't help, abort early
        # because there's not much useful we can do here.

        # Finally we get to the important bit: Each of these is a small change
        # to the floating point number that corresponds to a large change in
        # the lexical representation. Trying these ensures that our floating
        # point shrink can always move past these obstacles. In particular it
        # ensures we can always move to integer boundaries and shrink past a
        # change that would require shifting the exponent while not changing
        # the float value much.

        for g in [math.floor(self.current), math.ceil(self.current)]:
            self.consider(g)

        if self.consider(int(self.current)):
            self.debug('Just an integer now')
            self.delegate(
                Integer, convert_to=int, convert_from=float
            )
            return

        m, n = self.current.as_integer_ratio()
        i, r = divmod(m, n)

        # Now try to minimize the top part of the fraction as an integer. This
        # basically splits the float as k + x with 0 <= x < 1 and minimizes
        # k as an integer, but without the precision issues that would have.
        self.call_shrinker(
            Integer,
            i, lambda k: self.consider((i * n + r) / n),
        )
