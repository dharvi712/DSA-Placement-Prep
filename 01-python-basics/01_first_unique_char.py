"""
Problem   : First Unique Character
Topic     : Python Basics for DSA
Difficulty: Easy
Date      : 2026-08-01

Approach:
    Count frequency of each character using Counter (one pass), then
    scan the string again in order and return the index of the first
    character whose count is exactly 1. Two passes total, but each is
    O(n), so it stays linear overall.

Time Complexity : O(n) -> one pass to count, one pass to check
Space Complexity: O(k) -> k = number of distinct characters (<=26 for
                  lowercase letters, so effectively O(1) in practice)
"""

from collections import Counter


def first_unique_char(s):
    freq = Counter(s)
    for i, ch in enumerate(s):
        if freq[ch] == 1:
            return i
    return -1


if __name__ == "__main__":
    test_cases = [
        ("leetcode", 0),
        ("loveleetcode", 2),
        ("aabb", -1),
        ("", -1),
        ("z", 0),
    ]

    for i, (inp, expected) in enumerate(test_cases, 1):
        result = first_unique_char(inp)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i}: {status} | got={result} expected={expected}")
