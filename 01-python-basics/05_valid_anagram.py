"""
Problem   : Valid Anagram
Topic     : Python Basics for DSA
Difficulty: Easy
Date      : 2026-08-01

Approach:
    Two approaches shown for comparison.
    1) Sorting: if both strings are anagrams, sorting scrambles both
       into the exact same order (same letters -> same sorted result).
    2) Counter: build a frequency map of each string's characters and
       compare the two maps directly - anagrams have identical maps.

Time Complexity :
    - Sorting approach : O(n log n) -> dominated by sort
    - Counter approach : O(n)       -> single pass to build each Counter
Space Complexity:
    - Sorting approach : O(n) -> sorted() creates new lists
    - Counter approach : O(k) -> k = number of distinct characters

Counter is asymptotically better (O(n) vs O(n log n)). Sorting is
simpler to write/remember but strictly slower on large inputs.
"""

from collections import Counter


def is_anagram_sort(s1, s2):
    return sorted(s1) == sorted(s2)


def is_anagram_counter(s1, s2):
    return Counter(s1) == Counter(s2)


if __name__ == "__main__":
    test_cases = [
        (("listen", "silent"), True),
        (("eat", "tea"), True),
        (("cat", "cats"), False),
        (("cat", "dog"), False),
        (("", ""), True),
    ]

    for i, ((s1, s2), expected) in enumerate(test_cases, 1):
        r1 = is_anagram_sort(s1, s2)
        r2 = is_anagram_counter(s1, s2)
        status = "PASS" if (r1 == expected and r2 == expected) else "FAIL"
        print(f"Test {i}: {status} | sort={r1} counter={r2} expected={expected}")
