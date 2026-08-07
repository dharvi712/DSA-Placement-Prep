"""
Problem   : Remove Duplicates from Sorted Array
Topic     : Arrays & Strings - Two Pointers (slow/fast, same direction)
Difficulty: Easy
Date      : 2026-08-05

Approach:
    Unlike Valid Palindrome (opposite-ends pointers), this needs a
    DIFFERENT two-pointer pattern: both pointers start near the
    beginning and move in the SAME direction, at different speeds.
    `slow` marks the position where the next unique value should be
    written. `fast` scans ahead looking for the next value that
    differs from arr[slow]. Since the array is sorted, duplicates are
    always adjacent, so comparing arr[fast] to arr[slow] (the last
    confirmed-unique value) is enough - no need to compare against
    every previously-seen value.
    Modifies arr in-place - no extra array created, unlike a first
    attempt using a separate result list (which would cost O(n) space).

Time Complexity : O(n) -> fast scans the array once; slow only moves forward
Space Complexity: O(1) -> in-place, no extra array/structure used
"""


def remove_duplicates(arr):
    if not arr:
        return 0

    slow = 0  # position of the last unique value placed so far

    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]

    return slow + 1


if __name__ == "__main__":
    test_cases = [
        ([1, 1, 2, 2, 3], 3, [1, 2, 3]),
        ([1, 1, 1, 1], 1, [1]),
        ([1, 2, 3], 3, [1, 2, 3]),
        ([], 0, []),
    ]

    for i, (arr, expected_count, expected_prefix) in enumerate(test_cases, 1):
        count = remove_duplicates(arr)
        prefix = arr[:count]
        status = "PASS" if (count == expected_count and prefix == expected_prefix) else "FAIL"
        print(f"Test {i}: {status} | count={count} prefix={prefix} expected_count={expected_count} expected_prefix={expected_prefix}")
