"""
Problem   : Valid Palindrome
Topic     : Arrays & Strings - Two Pointers
Difficulty: Easy
Date      : 2026-08-05

Approach:
    Two pointers starting at opposite ends of the string, moving toward
    each other. At each step, compare s[left] and s[right]. If they
    ever don't match, it's not a palindrome - return False immediately.
    If they match, move both pointers inward. Loop continues while
    left < right (once pointers meet or cross, every pair has been
    checked with no mismatch, so it IS a palindrome).
    No need to convert to a list first - strings support direct
    indexing and comparison; we're never mutating characters, only
    reading and comparing them.

Time Complexity : O(n) -> each pointer moves at most n/2 times combined
Space Complexity: O(1) -> only two integer pointers, no extra structure
"""


def palindrome(s):
    left = 0
    right = len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1

    return True


if __name__ == "__main__":
    test_cases = [
        ("level", True),
        ("hello", False),
        ("a", True),
        ("", True),
        ("racecar", True),
        ("ab", False),
    ]

    for i, (inp, expected) in enumerate(test_cases, 1):
        result = palindrome(inp)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i}: {status} | got={result} expected={expected}")
