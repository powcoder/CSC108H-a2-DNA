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

from hypothesis.internal.compat import hrange
from hypothesis.internal.conjecture.shrinking.common import Shrinker, \
    find_integer


"""
This module implements a shrinker for non-negative integers.
"""


class Integer(Shrinker):
    """Attempts to find a smaller integer. Guaranteed things to try ``0``,

    ``1``, ``initial - 1``, ``initial - 2``. Plenty of optimisations beyond
    that but those are the guaranteed ones.
    """

    def short_circuit(self):
        for i in hrange(2):
            if self.consider(i):
                return True
        self.mask_high_bits()
        if self.size > 8:
            # see if we can squeeze the integer into a single byte.
            self.consider(self.current >> (self.size - 8))
            self.consider(self.current & 0xff)
        return self.current == 2

    def check_invariants(self, value):
        assert value >= 0

    def left_is_better(self, left, right):
        return left < right

    def run_step(self):
        self.shift_right()
        self.shrink_by_multiples(2)
        self.shrink_by_multiples(1)

    def shift_right(self):
        base = self.current
        find_integer(lambda k: k <= self.size and self.consider(
            base >> k
        ))

    def mask_high_bits(self):
        base = self.current
        n = base.bit_length()

        @find_integer
        def try_mask(k):
            if k >= n:
                return False
            mask = (1 << (n - k)) - 1
            return self.consider(mask & base)

    @property
    def size(self):
        return self.current.bit_length()

    def shrink_by_multiples(self, k):
        base = self.current

        @find_integer
        def shrunk(n):
            attempt = base - n * k
            return attempt >= 0 and self.consider(attempt)
        return shrunk > 0
