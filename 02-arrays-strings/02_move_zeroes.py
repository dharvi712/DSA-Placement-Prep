"""
Problem   : Move Zeroes
Topic     : Arrays & Strings - Two Pointers (slow/fast, same direction)
Difficulty: Easy
Date      : 2026-08-08
LeetCode  : #283 (Accepted)

Approach:
    Same slow/fast, same-direction pattern as Remove Duplicates, but
    adapted: instead of slow tracking "position of last unique value",
    slow tracks "position where the next non-zero value should go".
    fast scans every element; whenever fast finds a non-zero value AND
    slow is currently sitting on a zero, swap them - this pushes the
    non-zero value forward to slow's position while pushing the zero
    back to where fast was. Either way (swap happened or not), slow
    only advances once it's confirmed to be sitting on a non-zero
    value - meaning slow always marks the boundary of "confirmed
    non-zero region processed so far".
    Modifies nums in-place via swapping - no extra array needed.

Time Complexity : O(n) -> fast scans the array once; slow only moves forward
Space Complexity: O(1) -> in-place swaps, no extra array/structure used
"""


class Solution:
    def moveZeroes(self, nums: list) -> None:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0 and nums[slow] == 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
            if nums[slow] != 0:
                slow += 1


if __name__ == "__main__":
    test_cases = [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0], [0]),
        ([1, 0, 1], [1, 1, 0]),
        ([0, 0, 1], [1, 0, 0]),
    ]

    sol = Solution()
    for i, (inp, expected) in enumerate(test_cases, 1):
        arr = inp.copy()
        sol.moveZeroes(arr)
        status = "PASS" if arr == expected else "FAIL"
        print(f"Test {i}: {status} | got={arr} expected={expected}")
