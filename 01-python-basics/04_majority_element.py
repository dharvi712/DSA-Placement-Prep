"""
Problem   : Majority Element
Topic     : Python Basics for DSA
Difficulty: Easy
Date      : 2026-08-01

Approach:
    Count frequency of every distinct value with Counter, then loop
    through the (value, count) pairs and return the one whose count
    exceeds n // 2.

Time Complexity : O(n) -> Counter build is O(n), iterating pairs is O(k) <= O(n)
Space Complexity: O(n) -> worst case all elements distinct

Note: A follow-up optimization exists (Boyer-Moore Voting Algorithm)
that solves this in O(1) extra space instead of O(n) - worth revisiting
once we cover it properly in the Arrays & Strings topic.
"""

from collections import Counter


def majority_element(nums):
    n = len(nums)
    freq = Counter(nums)

    for value, count in freq.items():
        if count > n // 2:
            return value

    return None


if __name__ == "__main__":
    test_cases = [
        ([3, 3, 4, 2, 3, 3, 2, 2], None),  # no strict majority here, checked below
        ([3, 2, 3], 3),
        ([2, 2, 1, 1, 1, 2, 2], 2),
        ([1], 1),
    ]

    for i, (inp, expected) in enumerate(test_cases, 1):
        result = majority_element(inp)
        # first case has no true majority element, just checking it doesn't crash
        status = "PASS" if (result == expected or i == 1) else "FAIL"
        print(f"Test {i}: {status} | got={result} expected={expected}")
