https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
"""Test that `continue` is catched when met inside a `finally` clause."""

# pylint: disable=missing-docstring, lost-exception, broad-except

while True:
    try:
        pass
    finally:
        continue # [continue-in-finally]

while True:
    try:
        pass
    finally:
        break

while True:
    try:
        pass
    except Exception:
        pass
    else:
        continue
   