""" 
I need to do it again

Problem   : Target-Sum Subarray (custom problem, generalizes "Balanced
            Snack Packing" from target=0 to any target)
Topic     : Arrays & Strings - Prefix Sum + Hashing
Difficulty: Medium
Date      : 2026-08-05

Approach:
    Neither plain two-pointers (opposite ends) NOR sliding window work
    here, because the array can contain NEGATIVE numbers:
    - Opposite-ends two pointers don't apply - there's no meaningful
      "shorter side" concept like Container With Water; the pointers
      wouldn't represent anything physically meaningful for this problem.
    - Sliding window breaks because shrinking the window from the left
      isn't guaranteed to decrease the sum when negative numbers are
      involved (removing a negative number INCREASES the sum) - this
      breaks the monotonic guarantee sliding window depends on.

    Instead: track a running (prefix) sum while scanning once. At each
    index i, running_sum = sum of everything from index 0 to i.
    If running_sum[i] - running_sum[j] = target for some earlier index
    j, then the subarray from j+1 to i sums to exactly target.
    Rearranging: running_sum[j] = running_sum[i] - target.
    So at each step, compute `needed = running_sum - target` and check
    if that value was already seen as a running_sum at an earlier index
    (O(1) dict lookup) - this is the exact same "complement" pattern as
    Two Sum, just applied to running sums instead of raw values.

    seen = {0: -1} is seeded before the loop starts to correctly handle
    subarrays that start right at index 0 (running_sum of 0 conceptually
    occurs "before" the array begins, at index -1).

Time Complexity : O(n) -> single pass, O(1) average dict lookup/insert
Space Complexity: O(n) -> seen dict can hold up to n entries
"""


def has_subarray_with_sum(arr, target):
    seen = {0: -1}
    running_sum = 0

    for i, num in enumerate(arr):
        running_sum += num
        needed = running_sum - target
        if needed in seen:
            return True
        seen[running_sum] = i

    return False


if __name__ == "__main__":
    test_cases = [
        (([3, -2, 5, -1, 4], 6), True),                  # 5 + -1 + 4 = 8? check: -2+5-1+4=6 (idx1-4)
        (([1, 2, 3], 100), False),
        (([4, -1, -3, 2, -2, 1, -1], 0), True),           # matches Balanced Snack Packing, target=0
        (([6, 1, 2], 6), True),                            # tests the {0: -1} seed - subarray starting at index 0
        (([1, 2, 3], 6), True),                             # whole array sums to target
    ]

    for i, ((arr, target), expected) in enumerate(test_cases, 1):
        result = has_subarray_with_sum(arr, target)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i}: {status} | got={result} expected={expected}")
