https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
"""Test for duplicate-check."""

def main():
    """The second ValueError should be flagged."""
    try:
        raise ValueError('test')
    except ValueError:
        return 1
    except ValueError:  # [duplicate-except]
        return 2
    except (OSError, TypeError):
        return 3
