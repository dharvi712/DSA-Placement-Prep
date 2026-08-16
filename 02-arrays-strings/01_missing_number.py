"""
Problem   : Missing Number
Topic     : Arrays & Strings - Math trick (sum formula)
Difficulty: Easy
Date      : 2026-08-12
LeetCode  : #268

Approach:
    Array contains n distinct numbers from the range [0, n] (n+1
    possible values), but only has n slots - so exactly one value from
    that range is guaranteed to be missing.

    Key distinction that caused confusion while solving this: n here
    means len(nums) (the COUNT of elements), which is NOT the same as
    "the range [0, n]" - that range actually has n+1 possible values
    (0, 1, 2, ..., n). The range always has exactly one more possible
    value than the array has slots, which is structurally why exactly
    one number is always missing.
    Concrete check: nums=[0,1] -> n=len(nums)=2 -> range [0,2] =
    {0,1,2} = 3 possible values -> array holds 2 of them -> 2 missing.

    First idea considered: sort the array, walk through comparing
    index to value, wherever they mismatch signals roughly where the
    gap is. Rejected because:
    (a) sorting costs O(n log n), the sum approach below is O(n)
    (b) it needs an extra special case for when NOTHING mismatches
        inside the array's actual indices (e.g. [0,1] - both match
        perfectly) - in that case the missing number is n itself, one
        position past the array's last valid index. Can't just "check
        index n" directly either, since nums[n] doesn't exist for an
        array of length n (valid indices only go 0 to n-1) - would
        raise an IndexError.

    Sum-based approach avoids all of this entirely:
    - Sum of the COMPLETE range [0..n] = n*(n+1)/2 (known formula)
    - Sum of the ACTUAL array = sum(nums)
    - missing number = complete_sum - actual_sum
    Verified by hand: nums=[3,0,1] -> complete sum (range [0,3]) =
    0+1+2+3=6, actual sum=3+0+1=4, difference=2 -> matches expected.

Time Complexity : O(n) -> sum(nums) is a single O(n) pass; the formula
                  itself is O(1)
Space Complexity: O(1) -> only a few integer variables, no extra structure
"""


class Solution:
    def missingNumber(self, nums: list) -> int:
        n = len(nums)
        expected_sum = n * (n + 1) // 2
        actual_sum = sum(nums)
        return expected_sum - actual_sum


if __name__ == "__main__":
    test_cases = [
        ([3, 0, 1], 2),
        ([0, 1], 2),
        ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8),
        ([0], 1),
    ]

    sol = Solution()
    for i, (inp, expected) in enumerate(test_cases, 1):
        result = sol.missingNumber(inp)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i}: {status} | got={result} expected={expected}")
