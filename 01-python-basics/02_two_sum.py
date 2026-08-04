"""
Problem   : Two Sum
Topic     : Python Basics for DSA
Difficulty: Easy
Date      : 2026-08-01

Approach:
    Brute force would check every pair (O(n^2)). Instead, do a single
    pass: for each number, compute its "complement" (target - num) -
    the value that would complete the pair. Check if that complement
    was already seen (O(1) dict lookup). If yes, we found our pair.
    If no, store the current number -> index in `seen` for future
    iterations to find. Storing happens AFTER the check, so a number
    can never pair with itself in the same iteration.

Time Complexity : O(n) -> single pass, O(1) average dict lookup/insert
Space Complexity: O(n) -> seen dict can hold up to n entries
"""


def two_sum(nums, target):
    seen = {}  # value -> index

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return []


if __name__ == "__main__":
    test_cases = [
        (([2, 7, 11, 15], 9), [0, 1]),
        (([3, 2, 4], 6), [1, 2]),
        (([3, 3], 6), [0, 1]),
        (([5, 1, 4, 2], 6), [0, 1]),
        (([1, 2, 3], 100), []),
    ]

    for i, ((nums, target), expected) in enumerate(test_cases, 1):
        result = two_sum(nums, target)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i}: {status} | got={result} expected={expected}")
