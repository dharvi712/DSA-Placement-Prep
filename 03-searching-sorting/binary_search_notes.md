# Binary Search — My Notes

## 1. The Core Idea

Binary search doesn't require a sorted array. It only requires:

> At any `mid`, is there one cheap check whose answer lets me throw away an entire half of the search space, with 100% certainty?

Sortedness is just the most common way to get that guarantee. Other ways: "one half of a rotated array is always sorted," "uphill/downhill around a peak," "if speed X works, X+1 also works."

**Before applying binary search to any new problem, ask:**
1. What am I certain of, and what am I unsure of?
2. What's the search space — array indices, or a range of possible values/answers?
3. What cheap check can I run at `mid` that exploits my certainty?
4. Test the check on 2–3 tiny hand examples before trusting it.
5. Does my rule ever fail to make progress (infinite loop check)?
6. What does my invariant say when the loop ends — what do I return?

---

## 2. The Most Important Tool: The Loop Invariant

An **invariant** is a statement that stays TRUE before the loop starts, after every iteration, and when it ends. State it in one sentence before writing code — the code should be *forced* by the invariant, not memorized.

Example (basic search):
> "If the target exists, it's in `arr[low..high]`. It is NOT at any index `< low` or `> high`."

Whatever you do inside the loop must **preserve** this sentence. That's what tells you `low = mid+1` vs `low = mid`, `high = mid-1` vs `high = mid`, etc. — you don't guess these, you derive them.

---

## 3. Two Loop Templates — Pick One, Never Mix Them

### Template A — "Shrink to one, trust it directly"
Use when the invariant *guarantees* `low`'s final resting value is correct — no need to explicitly re-test it.

```python
low, high = 0, n
while low < high:
    mid = (low + high) // 2
    if condition(mid):
        high = mid       # mid might still be the answer — keep it alive
    else:
        low = mid + 1    # mid is definitely wrong — discard it fully
return low                # low == high, this IS the answer
```
Used for: lower_bound / first occurrence, insertion point problems.

### Template B — "Test every candidate, remember the best confirmed one"
Use whenever there's a `canX(mid)` yes/no simulation check and no airtight proof that `low` auto-lands correctly. **This is the default for the entire "search on the answer" family.**

```python
low, high = MIN_POSSIBLE, MAX_POSSIBLE
ans = high   # or low, a safe fallback
while low <= high:
    mid = low + (high - low) // 2
    if canX(mid):
        ans = mid
        high = mid - 1   # try to do even better (if minimizing)
    else:
        low = mid + 1
return ans
```

**Golden rule:** if you're tracking a separate `ans` variable, you MUST use `while low <= high`. Using `while low < high` here causes a bug — it skips testing the case `low == high`, silently missing the final candidate. (Found this bug myself while debugging Smallest Divisor — `low<high` returned a stale `ans` that never got confirmed as `1`.)

**Rule of thumb going forward:** for any "search on the answer" problem, always default to Template B.

---

## 4. Deriving Any New Invariant — Self-Questioning Checklist

Run through this on paper before writing code:

1. If `arr[mid]` equals/exceeds/is-less-than the target, is `mid` "definitely wrong" (discard) or "maybe the answer" (keep alive)?
2. If "maybe the answer" → that boundary keeps `mid` in range (`high = mid`, not `mid-1`).
3. If "definitely wrong" → safe to fully discard (`low = mid+1` or `high = mid-1`).
4. Trace the boundary case `low == high` (or adjacent) by hand — does your update ever leave `low`/`high` unchanged? If yes → infinite loop → fix the update.
5. Test your guessed rule against 3–4 concrete tiny examples, filling an actual table (mid, arr[mid], which half is sorted/valid, etc.) before trusting it.

---

## 5. Problems Solved & Their Core Insight

### Basic Search (LC 704)
Standard sorted array search. Invariant: target (if exists) is in `arr[low..high]`.

### Lower Bound / First Occurrence
Invariant: "everything before `low` is too small; everything from `high` onward is a valid candidate."
- `arr[mid] >= target` → maybe the answer → `high = mid`
- `arr[mid] < target` → discard → `low = mid + 1`
- Loop: `while low < high` (Template A), return `low`.

### Search in Rotated Sorted Array (LC 33)
**Key fact (self-derived and table-tested):** at any split, `arr[low] <= arr[mid]` is True **exactly when** the left half is sorted.
- If left sorted and target is within `[arr[low], arr[mid])` → search left.
- Else → search right (whichever half is sorted, use its known range to decide).

### Find Peak Element (LC 162)
**Key fact:** compare `arr[mid]` to `arr[mid+1]`.
- Uphill (`arr[mid] < arr[mid+1]`) → a peak is *guaranteed* to exist to the right → `low = mid+1`.
- Downhill (`arr[mid] > arr[mid+1]`) → a peak is at `mid` or to its left → `high = mid`.
- Why binary search applies at all: one comparison at `mid` always kills exactly one half — sortedness isn't required, only that guarantee.
- Simpler/slower alternative: O(n) linear scan checking both neighbors — fine if problem doesn't demand O(log n).

---

## 6. "Search on the Answer" Family (Template B)

**Pattern recognition:** the answer is a *number* (speed, capacity, days, largest-sum, divisor — not an array index), and there's a monotonic "does this value work?" check.

**General recipe:**
1. State the target as one number in one sentence ("minimum speed", "minimum capacity", etc.)
2. `low` = the smallest value that could ever conceivably work (often: the single largest "unit" that must fit, e.g. `max(weights)`, `max(bloomDay)` isn't right there — check per-problem)
3. `high` = the "do nothing clever" worst case (e.g. `sum(weights)`, `max(bloomDay)`, `sum(nums)`)
4. `canX(mid)`: simulate — walk the array once, greedily, exactly as if you were doing the task by hand with that fixed value.
5. Monotonicity check: "if X works, does X+1 (or X-1, depending on min/max) also work?" — must be able to say yes confidently, or binary search doesn't apply.
6. Minimizing → on success, record `ans=mid` and shrink `high=mid-1`. Maximizing → on success, record `ans=mid` and shrink `low=mid+1`.

### Koko Eating Bananas (LC 875)
- Search space: eating speed `k`.
- `low=1`, `high=max(piles)`.
- Check: sum of `ceil(pile/k)` over all piles `<= h`?
- Minimizing → success shrinks `high`.

### Capacity to Ship Packages Within D Days (LC 1011)
- Search space: ship capacity.
- `low = max(weights)` (heaviest single package sets the floor — anything smaller guarantees failure), `high = sum(weights)`.
- Check: greedily accumulate load per day, cut to a new day when adding the next package would exceed capacity; count days needed `<= days`?

### Minimum Days to Make m Bouquets (LC 1482)
- Search space: number of days waited.
- **Pre-check before binary search:** if `m * k > n`, return `-1` immediately (impossible regardless of days).
- `low = min(bloomDay)`, `high = max(bloomDay)`.
- Check: walk the array, track a *consecutive* "streak" of bloomed flowers (streak resets to 0 the moment a flower hasn't bloomed — adjacency matters!). Each streak contributes `streak // k` bouquets. Sum `>= m`?

### Find the Smallest Divisor Given a Threshold (LC 1283)
- Search space: divisor value.
- `low=1`, `high=max(nums)`.
- Check: sum of `ceil(num/mid)` over all nums `<= threshold`?
- **Bug I found & fixed myself:** used `low < high` with a separate `ans` var — caused the last candidate (`low==high`) to never be tested. Fixed by switching to `low <= high` (Template B).
- **LeetCode platform gotcha:** code must be wrapped in `class Solution:` with `self` as first param — this is a submission-format requirement, unrelated to the algorithm itself.

### Split Array Largest Sum (LC 410) — in progress
- Search space: the "max allowed subarray sum" cap.
- `low = max(nums)` (no subarray can have a smaller max than the single largest element), `high = sum(nums)`.
- Check: greedily accumulate a running subarray sum; cut to a new subarray when the next element would push the sum over `mid`; count pieces needed `<= k`?

### Divide Chocolate (LC 1231) — in progress
- Twist: this is a **maximization** problem (opposite direction from the others).
- `low = min(sweetness)`.
- `high` needs more care than just `sum(sweetness)` — since `k+1` non-empty pieces are required in total, a tighter bound is `sum(sweetness) // (k+1)`.
- Check: greedily cut a new piece the moment running sum `>= mid`; count pieces `>= k+1`?
- Maximizing → on success, shrink `low = mid + 1` (opposite of the minimizing problems).

### Sum of Mutated Array Closest to Target (LC 1300) — next up
- Twist: no clean "works/doesn't work" — it's about minimizing *distance* to a target, so the usual success/fail branching doesn't directly apply. Needs a different justification for why binary search still works (based on how the transformed sum changes monotonically with `cap`).

---

## 7. Mistakes I Made & Debugged Myself (worth remembering)

- **`high = mid` + `while low <= high`** → infinite loop when `low==high` (found via lower_bound trace). Fix: pair `high=mid` with `while low < high`.
- **`low = mid` on a failing check** → infinite loop when adjacent (`low=2,high=3`→`mid=2`, `low=mid` never advances). Fix: `low = mid + 1`.
- **`while low < high` combined with a separate `ans` variable** → last candidate never tested, wrong/stale answer returned. Fix: use `while low <= high` whenever tracking `ans`.
- **`return low` instead of `return ans`** → wrong when `low`'s converged value was never itself confirmed as a valid answer (only true safe under Template A's specific invariant).
- **LeetCode submission format** → must wrap solution in `class Solution:` with `self` param; a bare function causes `NameError: name 'Solution' is not defined` on their test harness.

---

## 8. Full Problem List for Practice (by tier)

**Tier 1 — classic array search:** 704, 35, 34, 744, 374

**Tier 2 — rotated / peak:** 33, 81 (dupes), 153, 154, 162 ✅, 852

**Tier 3 — 2D / multiple arrays:** 74, 240, 4 (Hard), 1385

**Tier 4 — search on the answer:** 875 ✅, 1011 ✅, 410 (in progress), 1231 (in progress), 1482 ✅, 1283 ✅, 1300 (next), 774 (Hard)

**Tier 5 — real-valued / unusual answer spaces:** 69, 287, 1901, revisit 4

Full official tag list: https://leetcode.com/problem-list/binary-search/binary search in 2D array
