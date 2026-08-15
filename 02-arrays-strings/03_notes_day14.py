"""
Topic     : Arrays & Strings - Day 14 Notes (Revision/debugging session +
            Missing Number - range vs length clarification)
Date      : 2026-08-12
Type      : Concept notes + bugs found and fixed while redoing old problems

======================================================================
TODAY WAS A "TYPING FROM MEMORY" STRESS TEST - REVISITED 4 OLD PROBLEMS
COLD, FOUND REAL BUGS, FIXED THEM. Documenting the bugs since the BUGS
are what taught me more than the working code would have.
======================================================================

------------------------------------------------------------
BUG SET 1: valid_anagram - step by step journey
------------------------------------------------------------
STEP 1 (wrong): s.sorted() == t.sorted()
  - .sorted() called AS A METHOD on the string itself
  - ERROR: strings don't have a .sorted() method at all

STEP 2 (question asked to self): is sorting a FUNCTION I call and
  pass the string INTO, or a METHOD I call ON the string? Recalled
  len(s) as the comparison - len() is a function, called as len(s),
  not s.len(). sorted() works the same way.

STEP 3 (fixed): sorted(s) == sorted(t)
  - sorted(s) is a built-in FUNCTION, takes s as input, RETURNS a
    new sorted list of characters - does not modify s itself

STEP 4 (improvement added on my own): before sorting at all, check
  if len(s) != len(t) first and return False immediately - two
  strings of different lengths can NEVER be anagrams, so this skips
  an unnecessary sort in that case (small optimization, not required
  but good instinct)

FINAL WORKING VERSION:
    def is_anagram(s, t):
        if len(s) != len(t):
            return False
        return sorted(s) == sorted(t)

------------------------------------------------------------
BUG SET 2: valid_palindrome - step by step journey (two rounds of bugs)
------------------------------------------------------------
STEP 1 (wrong): end = len(s)
  - used len(s) directly as the ending index
  - ERROR: for a string of length L, valid indices only go from 0 to
    L-1. len(s) itself is ONE PAST the last valid index - trying
    s[len(s)] would crash with an IndexError

STEP 2 (question asked to self): what index does the LAST character
  of a string actually sit at? Traced "level" (5 chars): indices are
  0,1,2,3,4 - the last one is index 4, which is len(s)-1 = 5-1 = 4.

STEP 3 (fixed): end = len(s) - 1

STEP 4 (wrong, second bug, different from the first): after fixing
  the index, wrote:
    if s[start] != s[end]:
        return False
        start += 1      <- this line placed AFTER return False
        end -= 1         <- same problem
    return True           <- placed INSIDE the if/while incorrectly,
                              at wrong indentation

STEP 5 (traced by hand to find the bug): walked through s="level"
  step by step. At start=0,end=4: s[0]='l', s[4]='l' - these MATCH,
  so the "if not equal" block is skipped entirely. But return True
  was sitting at a indentation level that made it run RIGHT AFTER
  that skipped if-check, on the very FIRST loop iteration - meaning
  the function would return True after checking just ONE character
  pair, never getting to check s[1] vs s[3].

STEP 6 (question asked to self): where should return True actually
  live so it only fires once the ENTIRE while loop finishes (not
  after one iteration)? Answer: it needs to be OUTSIDE the while loop
  entirely (same indentation as the word "while" itself), not nested
  inside it.
  Also: where should start+=1 and end-=1 go? They need to happen on
  EVERY iteration where characters matched (to keep moving inward),
  so they belong INSIDE the while loop but OUTSIDE the if block -
  never after a return (since return exits immediately, code after
  it in that block is unreachable and pointless).

STEP 7 (fixed, matches the correct Day 4 structure):
    def validpanidrome(s):
        start = 0
        end = len(s) - 1
        while start < end:
            if s[start] != s[end]:
                return False       # exits immediately on mismatch
            start += 1              # runs every iteration where matched
            end -= 1                 # (inside while, outside if)
        return True                  # only after full loop completes
                                       # with zero mismatches

LESSON: this was the SAME concept I already learned on Day 4, but it
still slipped when typing from memory today. Confirms that typing
code fresh (not copy-pasting) is what actually cements a pattern -
"having understood it once" and "being able to type it correctly cold"
are two different levels of knowing something.

------------------------------------------------------------
BUG SET 3: group_anagrams - step by step journey
------------------------------------------------------------
STEP 1 (wrong): seen[]
  - tried to declare some kind of empty structure with square
    brackets and nothing else
  - ERROR: not valid Python syntax at all, means nothing to the
    interpreter

STEP 2 (question asked to self, recalling Day 4): what structure did
  I use before that auto-creates an empty list for a brand-new key,
  so I can .append() immediately without a manual existence check?
  Recalled: defaultdict from the collections module.

STEP 3 (fixed, partially): from collections import defaultdict ...
  group = defaultdict()
  - progress, but STILL WRONG: called defaultdict() with nothing
    inside the parentheses

STEP 4 (question asked to self): what happens if I call
  group[key].append(word) on a key that doesn't exist yet, if
  defaultdict doesn't know what TYPE of empty value to create? Traced
  it: defaultdict() with no argument doesn't know to default missing
  keys to an empty LIST specifically - .append() would fail since
  there'd be nothing list-like to append onto.

STEP 5 (fixed): group = defaultdict(list)
  - passing the TYPE list tells defaultdict "when a new key shows up,
    auto-create it as an empty list"

STEP 6 (wrong): strs[i].sorted()
  - SAME mistake as valid_anagram - calling sorted as a method on the
    string instead of a function

STEP 7 (fixed): sorted(word)
  - also switched from index-based looping (for i in range(len(strs)))
    to value-based looping (for word in strs) since I never actually
    needed the index i for anything in this problem - only the VALUE
    of each word mattered (same lesson as the "for num in arr gives
    values not indices" note from Day 8)

STEP 8 (wrong): "".join was actually written as " ".join (space
  instead of empty string as the separator)
  - traced whether this breaks correctness: sorted("eat") and
    sorted("tea") both produce 3-letter results, so " ".join(...)
    would add spaces consistently between them - anagrams would still
    match each other correctly EVEN with this bug, since they always
    have the same length. Not a correctness bug for THIS specific
    problem, but not the intended/clean version either.

STEP 9 (fixed): "".join(sorted(word)) - empty string separator,
  matching the original correct Day 4 version exactly

FINAL WORKING VERSION:
    from collections import defaultdict
    def groupanagrams(nums):
        group = defaultdict(list)
        for word in nums:
            key = "".join(sorted(word))
            group[key].append(word)
        return list(group.values())

------------------------------------------------------------
BUG SET 4: two_sum - NOT YET FIXED, needs redo next session
------------------------------------------------------------
Original attempt mixed TWO different approaches together by accident:
- enumerate(nums, target) loop (doesn't make sense - target isn't a
  valid second argument to enumerate, that argument is a START INDEX
  for the counter, not a second iterable)
- a two-pointer while loop NESTED inside that enumerate loop
- return [] misplaced INSIDE the while loop at the same level as
  if/elif/else, meaning it would return [] after just the first
  comparison, regardless of whether a match was found

ROOT CAUSE: mixed up which approach to use. Plain Two Sum (array NOT
guaranteed sorted) needs the COMPLEMENT + DICT method from Day 1, NOT
the two-pointer method (that only works when the array is sorted, like
Two Sum II). Need to redo this cleanly using enumerate + a seen dict,
no two-pointer logic at all, since a plain unsorted array has no
"opposite ends" structure to exploit.

======================================================================
MISSING NUMBER (LC #268) - IN PROGRESS, key confusion resolved today
======================================================================
Problem: array of n distinct numbers in range [0, n] (n+1 possible
values), array only has n slots -> exactly one value missing. Find it.

MY FIRST IDEA: sort the array, walk through comparing index to value,
wherever they mismatch is (sort of) the missing number. VALID
DIRECTION but had real gaps:
1. O(n log n) from sorting - an O(n) approach exists (see below) and
   would be expected in an interview setting since no other
   constraint forces sorting.
2. Didn't handle the case where NOTHING mismatches inside the array's
   actual indices (e.g. nums=[0,1], sorted, indices 0 and 1 both
   match their values perfectly) - in that case the missing number is
   n itself (one past the last valid index), which needs a special
   case AFTER the loop, not found by mismatch-detection alone.

BIG CONFUSION TODAY, NOW RESOLVED: mixed up `n` (= len(nums), the
COUNT of elements) with "the range [0, n]" (which has n+1 POSSIBLE
values: 0,1,2,...,n). These are related but NOT the same number.
Concrete trace that fixed it: nums=[0,1] -> n=len(nums)=2 (2 elements)
-> range [0,2] = {0,1,2} = 3 possible values -> array only holds 2 of
them -> 2 is missing. The range always has exactly ONE MORE possible
value than the array has slots - that's structurally why exactly one
number is always guaranteed to be missing.

ALSO CLARIFIED: can't "loop index up to n+1" to catch the edge case,
because nums[n] doesn't exist for an array of length n (valid indices
only go 0 to n-1) - would cause an IndexError. The missing-at-the-end
case has to be handled as: "if the loop finishes with zero mismatches
found, the answer is n" (a separate check after the loop), not by
extending the loop's range further, since there's nothing there to
check against.

O(n) APPROACH (haven't coded yet, but derived the math):
Sum of complete range [0..n] = n*(n+1)/2 (known formula)
Sum of actual nums array = sum(nums)
Missing number = n*(n+1)/2 - sum(nums)
Verified by hand on nums=[3,0,1]: complete sum = 0+1+2+3 = 6,
actual sum = 3+0+1 = 4, difference = 2 -> matches expected answer.
Still need to verify on nums=[9,6,4,2,3,5,7,0,1] (expected answer 8)
and then actually write the code.

======================================================================
NEXT SESSION
======================================================================
- Redo Two Sum properly (complement + dict method, unsorted array)
- Finish Missing Number: verify the sum formula on example 3 by hand,
  then write the O(n) solution
- Quick-win streak problems suggested: Contains Duplicate (#217),
  Best Time to Buy/Sell Stock (#121), Single Number (#136, XOR trick)
"""
