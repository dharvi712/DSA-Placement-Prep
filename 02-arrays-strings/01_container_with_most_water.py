"""
Problem   : Container With Most Water
Topic     : Arrays & Strings - Two Pointers (opposite ends)
Difficulty: Medium
Date      : 2026-08-08
LeetCode  : #11 (Accepted)

Approach:
    Two pointers starting at opposite ends. At each step, compute the
    area = width * min(height[left], height[right]), and track the
    best seen so far. Width = right - left, so sorting the array first
    is NOT valid here (it would destroy the positional information
    width depends on) - unlike Twin Towers, where only the values
    mattered.

    Key insight for which pointer to move: the SHORTER side is always
    the bottleneck - water can never rise above it. Keeping the
    shorter side fixed and only moving the taller side's pointer can
    only shrink width while height stays capped at the same value, so
    the area can only stay the same or get worse. The only way to
    possibly find a taller height is to move away from the shorter
    line. So: always move the pointer at the shorter line inward.

    Area must be computed for EVERY (left, right) pair before deciding
    which pointer to move - not just when one specific condition is
    true - otherwise some pairs never get evaluated at all.

Time Complexity : O(n) -> left and right each move at most n times combined
Space Complexity: O(1) -> two pointers, one running max variable
"""


def container_with_water(heights):
    left = 0
    right = len(heights) - 1
    max_area = 0

    while left < right:
        area = (right - left) * min(heights[left], heights[right])
        max_area = max(max_area, area)

        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return max_area


if __name__ == "__main__":
    test_cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
    ]

    for i, (inp, expected) in enumerate(test_cases, 1):
        result = container_with_water(inp)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i}: {status} | got={result} expected={expected}")
