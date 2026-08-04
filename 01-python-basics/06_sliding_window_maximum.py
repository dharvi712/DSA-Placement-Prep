"""
Problem   : Sliding Window Maximum (intro version)
Topic     : Python Basics for DSA
Difficulty: Medium
Date      : 2026-08-01

Approach:
    Maintain a deque of INDICES, kept in decreasing order of their
    values, so the front of the deque is always the current window's
    max.
    - Before adding a new index, pop from the BACK any indices whose
      values are smaller than the current value - they can never be
      the max again while the current, larger value is still in the
      window (this keeps the deque small - O(n) total work, not O(n*k)).
    - Pop from the FRONT any index that has fallen outside the window
      (i.e. its index is too old relative to the current position).
    A deque (not a list) is required here because we need O(1)
    removal from BOTH ends: back (discard smaller candidates) and
    front (discard aged-out candidates). list.pop(0) would be O(n),
    silently making the whole algorithm slow again.

Time Complexity : O(n) -> each index is added and removed from the deque
                  at most once across the whole run
Space Complexity: O(k) -> deque holds at most k indices at a time
"""

from collections import deque


def sliding_window_max(nums, k):
    result = []
    dq = deque()  # stores indices, values kept in decreasing order

    for i, num in enumerate(nums):
        # remove indices outside the current window from the front
        while dq and dq[0] <= i - k:
            dq.popleft()

        # remove smaller values from the back - they're useless now
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


if __name__ == "__main__":
    test_cases = [
        (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]),
        (([4, 3, 2, 1], 2), [4, 3, 2]),
        (([9], 1), [9]),
    ]

    for i, ((nums, k), expected) in enumerate(test_cases, 1):
        result = sliding_window_max(nums, k)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i}: {status} | got={result} expected={expected}")
