"""
Topic     : Arrays & Strings - Day 9 Notes (Target-Sum Subarray, redone
            properly - set vs dict versions of the prefix-sum pattern)
Date      : 2026-08-09
Type      : Concept notes + mistakes made today + what I learned from them

======================================================================
THE BIG REALIZATION TODAY: SET vs DICT DEPENDS ON WHAT THE QUESTION ASKS
======================================================================
Redid Target-Sum Subarray from scratch and discovered something I
missed the first time: the {0: -1} DICT seed I used originally wasn't
actually necessary for THIS problem. A plain SET works just as well
(and is simpler) when the question only asks True/False.

RULE: 
- Question asks "DOES a valid subarray exist?" (True/False only)
  -> use a SET (values only, no index needed)
- Question asks "what is the LENGTH / POSITION / COUNT-WITH-LOCATION
  of a valid subarray?" -> use a DICT (value -> index), because you
  need the index to compute something (like a length via subtraction)

Both versions below solve the SAME core problem, just with different
data structures depending on what the final answer requires.

======================================================================
VERSION 1: SET-based (True/False only) - what this problem needed
======================================================================
def has_subarray_with_sum(arr, target):
    seen = {0}              # SET, seeded with 0 ("sum of nothing yet")
    running_sum = 0

    for num in arr:
        running_sum += num
        needed = running_sum - target
        if needed in seen:
            return True
        seen.add(running_sum)   # .add() for sets, NOT .append() (that's for lists)

    return False

======================================================================
VERSION 2: DICT-based (when you need length/position too)
======================================================================
def longest_subarray_with_sum(arr, target):
    seen = {0: -1}           # DICT, seeded so index -1 = "before array starts"
    running_sum = 0
    best_length = 0

    for i, num in enumerate(arr):        # need enumerate here - need the INDEX
        running_sum += num
        needed = running_sum - target
        if needed in seen:
            length = i - seen[needed]      # seen[needed] = the INDEX where that
                                             # running sum first occurred
            best_length = max(best_length, length)
        if running_sum not in seen:         # only store FIRST occurrence,
            seen[running_sum] = i            # keeps subarrays as long as possible

    return best_length

======================================================================
MISTAKES I MADE TODAY, REDOING THIS PROBLEM (and what fixed them)
======================================================================

MISTAKE: wrote seen = {0, -1}  (comma, no colon)
FIX: seen = {0: -1}  (colon, not comma)
WHY IT MATTERS: {0, -1} with a comma creates a SET containing two
separate elements (0 and -1) - completely different from a DICT with
one entry (key=0, value=-1). Comma vs colon inside {} is the entire
difference between "set of values" and "dict of key:value pairs" -
easy to miss visually but changes the data structure completely.

MISTAKE: tried to initialize running_sum = (first value of the array)
FIX: running_sum = 0
WHY IT MATTERS: running_sum represents "sum of everything seen SO FAR"
- before the loop starts, nothing has been processed yet, so it must
start at 0. The loop itself (running_sum += num) already adds the
first element once, when it's actually processed. Starting at the
first value AND adding it again in the loop would double-count it.

MISTAKE: wrote "running sum - target" with a SPACE in the variable name
FIX: running_sum - target (underscore, not space)
WHY IT MATTERS: Python variable names cannot contain spaces. A space
breaks the name into pieces and causes a syntax error - this is a
pure typo/carelessness issue, not a conceptual one, but worth being
careful about since it's an easy slip when typing fast.

CONFUSION: thought `needed` might represent an index, not a value
CLARIFIED: `needed` is ALWAYS a running-sum VALUE - specifically,
"what running sum would I need to have already seen, for a valid
subarray to end here." It is checked against `seen`, which (in the
set version) also only holds VALUES - so it's a consistent value-to-
value comparison, never an index lookup, in Version 1.

CONFUSION: what does seen[needed] mean, and how does i - seen[needed]
give a length?
CLARIFIED (only relevant to Version 2, the dict version):
seen[needed] looks up the INDEX stored under the key `needed` in the
dict. i - seen[needed] = "current position minus the position where
the matching running sum first occurred" = the number of elements in
between = the LENGTH of that subarray. Same subtraction idea as the
running-sum formula itself, just applied to positions instead of sums.

======================================================================
NEXT SESSION
======================================================================
- Subarray Sum Equals K (LC #560) - same pattern, but returns a COUNT
  of subarrays instead of True/False or length - will need a dict that
  counts OCCURRENCES of each running sum, not just first-seen index
- Squares of a Sorted Array (LC #977)
- 3Sum (LC #15) - extends Two Sum II
- OR: move to a new subtopic - in-place array manipulation
"""
