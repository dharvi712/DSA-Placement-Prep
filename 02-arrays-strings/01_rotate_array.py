"""
Problem   : Rotate Array
Topic     : Arrays & Strings - In-place manipulation (reversal-based)
Difficulty: Medium
Date      : 2026-08-09 (approx)
LeetCode  : #189

Approach:
    Naive approach (rotate one step at a time, k times) is O(n*k) -
    too slow for large k. Building a new rotated array via slicing is
    O(n) time but O(n) EXTRA space - violates "in-place" requirement.

    The reversal trick achieves O(n) time, O(1) extra space using
    THREE reversals:
        1. Reverse the whole array.
        2. Reverse the first k elements.
        3. Reverse the remaining n-k elements.

    Why it works: reversing the whole array correctly moves the last
    k elements to the front, but also reverses their internal order
    (and the internal order of the rest). Reversing each of the two
    resulting chunks separately undoes that unwanted internal reversal
    within each chunk, while leaving the chunks themselves swapped in
    position relative to each other - which is exactly a rotation.

    k = k % n handles k being larger than the array length - rotating
    n times brings the array back to its original state, so any full
    "lap" is redundant. E.g. rotating [1,2] by k=3 is the same as
    rotating by k=1 (3 % 2 = 1), since rotating by k=2 (a full lap for
    a 2-element array) would return it to the original order.

    reverse(arr, start, end) is a general two-pointer swap helper -
    same opposite-ends pattern as Valid Palindrome, but SWAPPING
    instead of comparing. Uses simultaneous tuple assignment
    (arr[start], arr[end] = arr[end], arr[start]) rather than a
    one-directional arr[start] = arr[end], which would silently
    overwrite and lose the original value at arr[start].

Time Complexity : O(n) -> each element is touched a constant number of
                  times across the three reversals combined
Space Complexity: O(1) -> in-place swaps only, no extra array
"""


def reverse(arr, start, end):
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1


def rotate(nums, k):
    n = len(nums)
    k = k % n

    reverse(nums, 0, n - 1)
    reverse(nums, 0, k - 1)
    reverse(nums, k, n - 1)

    return nums


if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4]),
        ([1, 2], 3, [2, 1]),
        ([-1, -100, 3, 99], 2, [3, 99, -1, -100]),
        ([1], 5, [1]),
    ]

    for i, (arr, k, expected) in enumerate(test_cases, 1):
        result = rotate(arr.copy(), k)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i}: {status} | got={result} expected={expected}")
