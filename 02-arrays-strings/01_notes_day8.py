"""
Topic     : Arrays & Strings - Day 8 Notes (Two Sum II + Prefix Sums)
Date      : 2026-08-09
Type      : Concept notes + small realizations worth remembering

======================================================================
WHAT `self.xxx` ACTUALLY MEANS (re-explained, finally clicked)
======================================================================
`self` refers to "this specific object" - the particular instance of
the class currently being worked with (e.g. one specific NumArray).

Anything assigned WITHOUT self. inside a method (e.g. `prefix = [0]`
instead of `self.prefix = [0]`) is a LOCAL variable - it only exists
while that one method is running, and is thrown away completely the
moment the method returns. Other methods on the same object have NO
way to see it - it's gone.

Anything assigned WITH self. (e.g. `self.prefix = [0]`) is attached to
the OBJECT ITSELF, not to the method. It persists for as long as the
object exists, and every method on that object (via `self.`) can read
and modify it.

Concrete rule: if something built in __init__ needs to be USED LATER
by a different method (like sumRange using prefix data built in
__init__), it MUST be stored as self.something in __init__. If it's
only ever needed within the one method that creates it, a plain local
variable is fine and self. isn't needed.

Same exact pattern as self.items in the Stack class from Day 1 - just
applied to a different attribute name (self.prefix here).

======================================================================
TWO SUM II - WHY TWO POINTERS INSTEAD OF THE DICT METHOD
======================================================================
Two Sum II adds ONE constraint that plain Two Sum (Day 1) didn't have:
"must use only constant extra space" - explicitly stated, not just
implied.

The dict/complement method from Day 1 would still give the CORRECT
answer here, but it uses O(n) space (the dict can grow up to n
entries) - which VIOLATES the explicit O(1) space constraint, even
though the array being sorted doesn't break the dict approach itself.

Because the array is already SORTED, opposite-ends two pointers work
here (same pattern as two_sum_sorted / Container With Water):
  - sum too small -> move left forward (need a bigger number)
  - sum too big -> move right backward (need a smaller number)
Uses only 2 integer variables -> genuinely O(1) space.

LESSON: "would this technique give the right answer" and "does this
technique satisfy ALL stated constraints" are two different questions.
Always check space/time constraints explicitly stated in a problem,
not just whether an approach would produce a correct result.

Also: this problem wants 1-INDEXED output (not standard 0-indexed).
Do all the actual pointer logic normally (0-indexed), and only add +1
to both indices at the very end, right before returning:
    return [left + 1, right + 1]

======================================================================
PREFIX SUMS - THE "PREPEND A ZERO" TRICK
======================================================================
Two ways to define a prefix sum array:

1) prefix[k] = sum of nums[0..k]  (straightforward version)
   - sumRange(i, j) = prefix[j] - prefix[i-1]
   - BUT this breaks when i=0, since prefix[-1] means something
     unexpected in Python (last element, not "nothing").

2) prefix[k] = sum of nums[0..k-1], with prefix[0] = 0 seeded first
   (the "prepend a zero" trick - same seeding idea as the {0: -1}
   trick from the target-sum-subarray problem a few days ago - both
   are about representing "nothing summed yet" cleanly instead of
   needing a special-case check).
   - prefix ends up ONE ELEMENT LONGER than nums.
   - sumRange(i, j) = prefix[j+1] - prefix[i]  <- no i-1, no edge case
   - Building it: start with self.prefix = [0], then for each num in
     nums: self.prefix.append(self.prefix[-1] + num)
     (self.prefix[-1] = last element added so far, reused pattern
     from Twin Towers' heights_sorted[-1]/[-2] indexing)

Example:
    nums   =    [4,  2,  5,  1,  3]        length 5
    prefix = [0, 4,  6, 11, 12, 15]        length 6 (nums length + 1)

    sumRange(1, 3) should be nums[1]+nums[2]+nums[3] = 2+5+1 = 8
    = prefix[3+1] - prefix[1] = prefix[4] - prefix[1] = 12 - 4 = 8  correct

LESSON: whenever a "sum from index 0 up to here" structure is involved
and index-0 edge cases keep needing special handling, check if
seeding/prepending a base value (0 for sums, or {0: -1} for a dict of
sums-seen) removes the edge case entirely instead of writing an if
statement for it.

======================================================================
NEXT SESSION
======================================================================
- Finish NumArray class (sumRange method) and get it accepted on
  LeetCode (#303)
- More prefix sum practice problems
- Continue toward Sliding Window (formalized) and in-place array
  manipulation
"""
