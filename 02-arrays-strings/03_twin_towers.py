"""
Problem   : Twin Towers (custom problem)
Topic     : Arrays & Strings
Difficulty: Medium
Date      : 2026-08-05

Approach:
    Unlike Container With Most Water, this problem has NO width/distance
    factor - only the two height VALUES matter, positions are irrelevant.
    So the answer is simply min(largest_value, second_largest_value)
    across the whole array (duplicates count as separate towers - if
    the max value appears twice, both "copies" are valid picks, so the
    answer can be the max value itself, e.g. [8,8,1,2,3] -> 8).

    Two viable approaches:
    1) Sort the array, take min of the last two elements - O(n log n).
       Valid here (unlike Container With Water) because index order
       genuinely doesn't matter to the answer.
    2) Single pass, O(n): track `highest` and `second_highest` as
       running variables.
       - If num > highest: the OLD highest must slide down into
         second_highest BEFORE highest is overwritten (order matters -
         once highest is overwritten, the old value is lost).
       - elif num > second_highest (but not > highest): only
         second_highest updates.
       - second_highest is always <= highest by construction, so
         min(highest, second_highest) always simplifies to just
         second_highest - no min() call actually needed at the end.

Time Complexity : O(n) for the single-pass approach (used below);
                  O(n log n) if sorting instead
Space Complexity: O(1) -> two running variables only, no extra structure
"""


def twin_towers(heights):
    highest = float('-inf')
    second_highest = float('-inf')

    for num in heights:
        if num > highest:
            second_highest = highest
            highest = num
        elif num > second_highest:
            second_highest = num

    return second_highest


# Alternative O(n log n) approach, kept for comparison:
def twin_towers_sorting(heights):
    heights_sorted = sorted(heights)
    return min(heights_sorted[-1], heights_sorted[-2])


if __name__ == "__main__":
    test_cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 8),   # two towers of height 8 exist
        ([8, 8, 1, 2, 3], 8),
        ([5, 5], 5),
        ([1, 2, 3, 4, 5], 4),
    ]

    for i, (inp, expected) in enumerate(test_cases, 1):
        r1 = twin_towers(inp)
        r2 = twin_towers_sorting(inp)
        status = "PASS" if (r1 == expected and r2 == expected) else "FAIL"
        print(f"Test {i}: {status} | single_pass={r1} sorting={r2} expected={expected}")
