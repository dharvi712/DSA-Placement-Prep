"""
Topic     : Python Basics for DSA - Time & Space Complexity
Date      : 2026-07-31
Type      : Concept notes (no coding yet - complexity analysis drills)

======================================================================
KEY TAKEAWAYS FROM TODAY
======================================================================

1. BIG O BASICS
   - Big O describes how runtime/memory grows as input size (n) grows,
     not exact seconds.
   - Drop constants:        O(2n)      -> O(n)
   - Drop lower-order terms: O(n^2 + n) -> O(n^2)
   - Different inputs get different variables:
     looping over two separate lists of size n and m -> O(n + m) or
     O(n * m), NOT O(n^2) unless n == m.

2. LOG N vs N LOG N
   - O(log n): input shrinks each step (usually halved), and O(1) work
     is done per step.  e.g. binary search.
   - O(n log n): either
       a) a loop of n items, each doing an O(log n) operation
          (e.g. binary search called n times), OR
       b) recursive halving where O(n) work happens at EVERY level
          (e.g. merge sort - splitting is log n levels deep, but each
          level still touches all n elements during merge).
   - Test: count how many levels/halvings happen (-> log n part), then
     separately check how much work happens AT each level
     (constant -> log n total; scales with n -> n log n total).

3. RECURSION COMPLEXITY IS NOT AUTOMATICALLY LOG N
   - Recursion's complexity depends on TWO things:
       1. How much the input shrinks per call
       2. How many recursive calls happen per level (branching factor)
   - Example: g5(n) below LOOKS like log n (input halves each call)
     but actually branches into 2 calls per level -> total calls sum
     to 1+2+4+...+n = O(n), NOT O(log n).

        def g5(n):
            if n <= 1:
                return
            g5(n // 2)
            g5(n // 2)

   - Counter-example showing recursion CAN be plain O(n):
        def sum_list(lst):
            if len(lst) == 0:
                return 0
            return lst[0] + sum_list(lst[1:])
     Shrinks by 1 each call, 1 call per level -> O(n) total, just like
     a loop written recursively.
   - RULE: "recursion = log n" is a false pattern-match. Always trace
     (a) shrink rate and (b) branching factor separately.

4. THE "HIDDEN NESTED LOOP" TRAP
   - `x in some_list` is O(k) where k = current list length (linear
     scan). It is NOT O(1) like `x in some_set` or `x in some_dict`.
   - This means a single visible `for` loop can secretly be O(n^2) if
     each iteration does a membership check against a growing list:

        def g3(lst):
            result = []
            for x in lst:
                if x not in result:      # O(k) scan, k grows 0..n-1
                    result.append(x)
            return result
        # Total scanning work = 0+1+2+...+(n-1) = n(n-1)/2 -> O(n^2)

   - FIX: swap the list for a set for the membership check (O(1) each)
     -> drops the whole function to O(n):

        def g3_fast(lst):
            seen = set()
            result = []
            for x in lst:
                if x not in seen:        # O(1) now
                    seen.add(x)
                    result.append(x)
            return result

   - GENERAL LESSON: "trade an O(n) list scan for an O(1) set/dict
     lookup" is one of the most common O(n^2) -> O(n) optimizations
     in interviews.

5. LIST OPERATION COMPLEXITIES (why they are what they are)
   Python lists are contiguous blocks of memory - this single fact
   explains everything below.

   | Operation           | Complexity | Why |
   |----------------------|-----------|-----|
   | lst.append(x)        | O(1) amortized | usually a free slot exists at the end; occasional resize+copy is O(n) but rare enough to average out to O(1) over many appends |
   | lst.insert(0, x)      | O(n)      | every existing element must shift right by 1 to make room at the front |
   | lst.pop()             | O(1)      | removes from the end, nothing else needs to shift |
   | lst.pop(0)            | O(n)      | every remaining element must shift left by 1 to close the gap |
   | lst[i]                | O(1)      | direct memory address calculation, no scanning |
   | lst.index(x)          | O(n)      | linear scan until match found |
   | x in lst              | O(n)      | linear scan, no hashing backing a plain list |

   AMORTIZED O(1) explained precisely:
   - NOT "always instant". Means: total cost of n appends, averaged
     over all n, stays constant even though occasional individual
     appends cost O(n) (resize + copy). Resizes get exponentially
     rarer as capacity doubles each time, which is what keeps the
     long-run average pinned at O(1).
   - This is fundamentally different from `x in lst`, which has NO
     rare/common split to average - it is a linear scan EVERY single
     call, with no exceptions. That's why append gets the "amortized"
     label and `in` does not.

======================================================================
MISTAKES I MADE TODAY (for future review)
======================================================================
- Called `x not in result` (list) an O(1) check - it's actually O(k),
  a hidden linear scan. This is what causes g3 to be O(n^2), not O(1).
- Assumed g5(n) [2 recursive calls, each on n//2] was O(log n) because
  the input halves each call. Missed that branching factor of 2
  cancels the halving out, making it O(n) total calls instead.
- Initial answer for merge-sort-style recursion (O(n log n)) was
  correct, but reasoning said "n = number of merges" instead of the
  more precise "n = total work redone at EACH of the log n levels".

======================================================================
NEXT SESSION
======================================================================
- Part C: list operation complexities fill-in-the-blank (11-18)
- Then start Topic 1 practice problems (Two Sum, Group Anagrams,
  Majority Element, Valid Anagram, Sliding Window Max, Custom Stack)
"""
