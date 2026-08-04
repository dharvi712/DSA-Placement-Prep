"""
Problem   : Group Anagrams
Topic     : Python Basics for DSA
Difficulty: Medium
Date      : 2026-08-01

Approach:
    Two words are anagrams if and only if they contain the exact same
    letters with the exact same frequency, just rearranged. Sorting a
    word's letters gives a canonical form that is IDENTICAL for every
    anagram of that word (e.g. "eat", "tea", "ate" all sort to "aet").
    Use that sorted string as a dict key, and group original words
    under it. defaultdict(list) auto-creates the empty list for a new
    key, avoiding a manual "if key not in group" check.

Time Complexity : O(n * k log k) -> n words, each sorted (k = avg word length)
Space Complexity: O(n * k) -> storing all words across all groups
"""

from collections import defaultdict


def group_anagrams(words):
    groups = defaultdict(list)

    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)

    return list(groups.values())


if __name__ == "__main__":
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    print(result)
    # Expected groups (order may vary): [['eat','tea','ate'], ['tan','nat'], ['bat']]

    # Sanity check: every group should have equal-length sorted words
    for group in result:
        keys = {"".join(sorted(w)) for w in group}
        assert len(keys) == 1, f"Group {group} is not all anagrams of each other!"
    print("All groups verified as valid anagram sets.")
