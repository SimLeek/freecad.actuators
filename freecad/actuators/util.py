"""
Utility functions for the BLDC motor visualization.
"""
def traverse_tuple(nums):
    """Automatically handles backwards iteration for range."""
    start, end = nums
    if start <= end:
        for i in range(start, end):
            yield i
    else:
        for i in range(start, end, -1):
            yield i