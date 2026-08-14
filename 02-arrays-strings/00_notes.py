 """
 revide all
Topic     : Arrays & Strings - Day 4 Notes
Date      : 2026-08-05
Type      : Concept notes + debugging lessons (small things that tripped
            me up today, worth remembering)

======================================================================
TWO POINTER PATTERNS - TWO DIFFERENT SHAPES, NOT ONE TRICK
======================================================================

1) OPPOSITE ENDS, MOVING INWARD
   - left starts at 0, right starts at len(arr)-1
   - used when the answer depends on a relationship between the
     OUTERMOST remaining elements (a pair), and shrinking the range
     from both sides makes sense
   - examples: Valid Palindrome (compare s[left] vs s[right]),
     Container With Most Water (width = right - left, height = shorter
     side), Meeting Room Doorway (sum values as pointers close in)
   - loop condition: while left < right (once they meet/cross, every
     pair has been checked)

2) SAME DIRECTION, DIFFERENT SPEEDS (slow/fast)
   - both pointers start near the beginning, move the SAME direction
   - used for FILTERING / REARRANGING in-place based on a property
     (duplicate/unique, zero/non-zero)
   - slow = position where the next "good" value should be written
   - fast = scans ahead looking for the next "good" value
   - examples: Remove Duplicates (slow tracks last unique value's
     position), Move Zeroes (slow would track next non-zero position)

HOW TO DECIDE WHICH ONE APPLIES (question to ask BEFORE coding):
"Is this problem about a PAIR of elements from opposite regions of the
array (-> opposite ends), or about REARRANGING elements based on some
property (-> same direction filtering)?"

======================================================================
MY OWN BUGS TODAY (things that actually tripped me up)
======================================================================

BUG: left += left  (instead of left += 1)
   - this DOUBLES left (1 -> 2 -> 4 -> 8...) instead of moving it
     forward by one step. Made this mistake twice today (Remove
     Duplicates attempt, then again in Container With Water attempt).
   - same bug pattern for right -= right (zeroes right out immediately
     instead of decrementing by 1)
   - LESSON: always read += and -= literally - "x += x" means
     "x = x + x", not "x = x + 1"

BUG: using { } and i++ (Java/C++ syntax) instead of Python syntax
   - Python has NO curly braces for blocks - uses indentation only
   - Python has no ++ operator at all - use x += 1
   - for loop syntax: for i in iterable:  (no parentheses, colon at end)

BUG: writing an if with no else, when both cases need handling
   - Container With Water: had `if arr[left] < arr[right]: ... ` with
     NO else branch. When the condition was False, NOTHING happened
     inside the loop - left and right never moved - infinite loop.
   - LESSON: if a variable MUST change every iteration for a loop to
     terminate, check that EVERY branch (if AND else) actually moves
     something. An if with no matching else is a red flag if the loop
     depends on state changing every time.

BUG: appending to a list and calling max() at the end, instead of
     tracking a single running "best so far" variable
   - not wrong, just wasteful - O(n) extra space for no reason when
     one variable (updated with max(current_best, new_value) inline)
     does the same job in O(1) space.

======================================================================
WHY min(8, 8) = 8, NOT AN ERROR (Twin Towers confusion)
======================================================================
min() does not require strict "less than" - it just returns whichever
is smaller OR EQUAL. If both values are identical, there's no smaller
one to pick, so it just returns that shared value. Two towers can have
the SAME height and still be two valid, DIFFERENT towers (different
positions) - a duplicate height is not "the same tower twice."

======================================================================
WHY SORTING BREAKS CONTAINER WITH WATER BUT NOT TWIN TOWERS
======================================================================
Container With Water: width = right - left depends on ORIGINAL INDEX
POSITIONS. Sorting destroys position information, so width becomes
meaningless after sorting. Cannot sort here.

Twin Towers: the answer only depends on the two height VALUES, not
their positions (the problem never asks WHICH towers, just the
strength value). So sorting is perfectly safe here - a completely
different problem shape even though both involve pairs of numbers in
an array. LESSON: don't assume a technique transfers just because two
problems "feel similar" - check what the answer actually depends on
(values only, vs values + positions).

======================================================================
WHY SLIDING WINDOW BREAKS WITH NEGATIVE NUMBERS
======================================================================
Sliding window (expand right / shrink left) depends on a MONOTONIC
guarantee: adding an element always increases the sum, removing an
element always decreases it. This only holds when all numbers are
POSITIVE. With negative numbers, removing a negative number from the
left of a window INCREASES the sum instead of decreasing it - breaks
the whole "shrink to reduce" logic. Confirmed this myself: window
[-2, 5, -1] sum = 2, removing -2 gives sum = 6 (WENT UP, not down).
LESSON: before reaching for sliding window, check "are all numbers
non-negative?" If not, sliding window's core assumption is broken.

======================================================================
PREFIX SUM + DICT PATTERN (target-sum subarray, generalizes to any target)
======================================================================
Neither opposite-ends two-pointers NOR sliding window work when the
array has negatives AND you need arbitrary contiguous-range sums.
Instead: track running_sum while scanning ONCE. At each index i:
    running_sum[j] = running_sum[i] - target
      (rearranged from: running_sum[i] - running_sum[j] = target)
This is the EXACT SAME algebraic move as Two Sum's
complement = target - num - just applied to running sums instead of
raw array values.

seen = {0: -1} MUST be seeded before the loop. Why: a subarray that
starts at index 0 has "nothing before it" - conceptually a running sum
of 0 occurring at index -1 (one position before the array starts).
Proved this myself: without the seed, has_subarray_with_sum([6,1,2], 6)
incorrectly returns False even though [6] alone sums to target,
because running_sum=0 (the "nothing summed yet" state) was never
recorded anywhere to be found.

======================================================================
"for num in arr" GIVES VALUES, NOT INDICES - don't index into it again
======================================================================
Mixed this up during Twin Towers: wrote `arr[nums]` inside a
`for num in heights:` loop, treating `num` as if it were an index.

Two different loop styles give DIFFERENT things:

    for num in heights:
        # num IS the actual VALUE at each step (e.g. 8, 1, 6...)
        # NOT an index - there is nothing to index into again here

    for i in range(len(heights)):
        # i IS an index (0, 1, 2...)
        # need heights[i] to get the actual value

    for i, num in enumerate(heights):
        # i = index, num = value at that index - get BOTH at once

RULE: if the loop variable came from `for x in some_list:` directly,
`x` is already a VALUE - never write `some_list[x]`, that's indexing
with a value instead of an index, which is either a bug or a crash
(e.g. heights[8] when 8 isn't a valid index, or silently wrong if it
happens to be a valid index that means something else entirely).

Only use square-bracket indexing (`arr[i]`) when the loop variable is
genuinely an index - i.e. it came from `range(...)` or the first part
of `enumerate(...)`, not from looping over the list's values directly.

When to pick which loop style, based on what today's problems needed:
- Twin Towers: only needed VALUES, positions never mattered to the
  answer -> `for num in heights:` was correct, no index needed at all.
- Two Sum (Day 1): needed BOTH the value AND its index (to return
  positions in the answer) -> needed `enumerate(nums)`.
- Remove Duplicates: needed an index (`fast`) specifically to be able
  to WRITE to a position (`arr[slow] = arr[fast]`) -> needed
  `for fast in range(1, len(arr)):`, not a plain value loop, because
  modifying the array in place requires index-based access.

======================================================================
NEXT SESSION
======================================================================
- Finish Container With Most Water (if/else structure, both branches)
- Move Zeroes (slow/fast pattern, slow tracks "next non-zero slot")
- More Two Pointers practice: Two Sum II, Squares of Sorted Array,
  Reverse String, 3Sum ,two sum sorted ii
"""
revise
