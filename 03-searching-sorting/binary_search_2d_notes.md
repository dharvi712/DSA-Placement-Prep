# Binary Search on 2D Matrices — Notes

## Core Idea

A 2D matrix doesn't need to be "sorted" in the traditional sense to binary search it. The real requirement (same as 1D): **at any point, is there one cheap check that lets me eliminate a whole chunk of the search space with certainty?** In 2D, that chunk might be half a flattened array, or a whole row, or a whole column — the pattern depends on the matrix's structure.

**Before applying any pattern, ask:**
1. Is the matrix fully flattenable into one sorted line, or only row+column sorted independently, or not sorted at all?
2. Am I searching for a specific value, or for a *rank* (k-th smallest), or for a *peak*?
3. Which corner (if using a staircase) gives me two opposite-effect directions from one comparison?

---

## Pattern 1: Fully Sorted Matrix → Flatten + 1D Binary Search

**When it applies:** every row sorted, AND each row's first element > previous row's last element (so reading row-by-row gives one fully sorted sequence).

**Technique:** treat the matrix as a flattened 1D array of size `rows*cols`. Binary search normally, converting the 1D `mid` index to 2D coordinates:
```python
row, col = mid // cols, mid % cols
```
- `mid // cols`: how many complete rows fit before this index → that's the row.
- `mid % cols`: what's left after removing those full rows → the column offset.

```python
def searchMatrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    rows, cols = len(matrix), len(matrix[0])
    low, high = 0, rows * cols - 1
    while low <= high:
        mid = (low + high) // 2
        row, col = mid // cols, mid % cols
        val = matrix[row][col]
        if val == target:
            return True
        elif val < target:
            low = mid + 1
        else:
            high = mid - 1
    return False
```

Everything except the `row, col = mid//cols, mid%cols` line is identical to plain 1D binary search (LC 704).

**LeetCode:** 74 — Search a 2D Matrix. Complexity: O(log(rows×cols)).

---

## Pattern 2: Row-Sorted AND Column-Sorted (not flattenable) → Staircase Search

**When it applies:** every row sorted left-to-right, every column sorted top-to-bottom, but NO guarantee across rows (e.g. row 2 might start smaller than row 1 ends). Flattening breaks here.

**Technique — start from top-right corner:**
- `val == target` → found.
- `val > target` → everything below in this column is even bigger (column ascending) → eliminate the column → move **left**.
- `val < target` → everything left in this row is even smaller (row ascending) → eliminate the row → move **down**.

**Why top-right, not top-left:** from top-left, both "move right" and "move down" *increase* the value — one comparison can't tell you which way to go. From top-right, "move left" decreases and "move down" increases — opposite effects from one corner, so one comparison cleanly picks a direction.

```python
def searchMatrix2(matrix, target):
    if not matrix or not matrix[0]:
        return False
    row, col = 0, len(matrix[0]) - 1   # top-right corner — NOTE: len(matrix[0]), not len(matrix)!
    while row < len(matrix) and col >= 0:
        val = matrix[row][col]
        if val == target:
            return True
        elif val > target:
            col -= 1
        else:
            row += 1
    return False
```

**Bug I actually hit:** used `len(matrix)-1` for the starting column instead of `len(matrix[0])-1`. `len(matrix)` = number of rows; `len(matrix[0])` = number of columns. Mixing these only breaks on non-square matrices — worth double-checking every time.

**LeetCode:** 240 — Search a 2D Matrix II. Complexity: O(rows + cols) — NOT full log-time; each step eliminates one row or column, not half the space.

---

## Pattern 3: Rows Individually Sorted Only → Binary Search Per Row

**When it applies:** each row is sorted, but rows have no relationship to each other (can't flatten, can't staircase).

**Technique:** run a normal 1D binary search (e.g. lower-bound style) independently on each row, track the best result across all rows.

```python
def leftMostColumnWithOne(matrix):
    rows, cols = len(matrix), len(matrix[0])
    best_col = cols
    for r in range(rows):
        low, high = 0, cols - 1
        while low < high:
            mid = (low + high) // 2
            if matrix[r][mid] == 1:
                high = mid
            else:
                low = mid + 1
        if matrix[r][low] == 1:
            best_col = min(best_col, low)
    return best_col if best_col != cols else -1
```

**LeetCode:** 1428 — Leftmost Column with at Least a One (Premium). Complexity: O(rows × log cols) — this is binary search *applied to* a matrix, not a single unified 2D search.

---

## Pattern 4: Binary Search on VALUE, Staircase as a Counting Subroutine

**When it applies:** same shape as Pattern 2 (rows + columns sorted), but the question is "what's the k-th smallest *value*", not "does target X exist." Rank ≠ flattened position in this matrix shape — Pattern 1's trick does NOT give correct ranks here (row-major order is not the same as value-sorted order).

**Technique — this is the "search on the answer" family (same as Koko/Ship Packages) applied to a grid:**
1. Search space: possible **values**, not indices. `low = matrix[0][0]`, `high = matrix[n-1][n-1]`.
2. Check function: "how many elements are `<= mid`?" — computed via a staircase walk, O(n) per check.
3. Monotonicity: if count-at-mid `>= k`, the k-th smallest is `<= mid` — increasing mid never decreases the count, so binary search is valid.
4. This is a lower-bound search → Template A (`low < high`, `high = mid` on success, return `low`).

**The count staircase — starts bottom-left this time** (opposite corner from Pattern 2, because we need "right = more qualify" and "up = smaller"):
```python
def kthSmallest(matrix, k):
    n = len(matrix)
    low, high = matrix[0][0], matrix[n-1][n-1]

    def countLessEqual(mid):
        count = 0
        row, col = n - 1, 0   # bottom-left
        while row >= 0 and col < n:
            if matrix[row][col] <= mid:
                count += row + 1   # this cell + everything above it in the column
                col += 1
            else:
                row -= 1
        return count

    while low < high:
        mid = low + (high - low) // 2
        if countLessEqual(mid) >= k:
            high = mid
        else:
            low = mid + 1
    return low
```

`count += row + 1`: since the column is sorted ascending, once `matrix[row][col] <= mid`, every cell above it (row+1 cells total, including itself) also qualifies — count a whole slice in one shot instead of checking each cell.

**LeetCode:** 378 — Kth Smallest Element in a Sorted Matrix. Complexity: O(log(value range) × (rows+cols)).

---

## Pattern 4b: Staircase Reused for Counting (not searching for one target)

Same staircase skeleton as Pattern 2, but accumulate a count instead of early-returning on match. Direction rules must be re-derived from the matrix's actual sort order (ascending vs descending) — don't copy Pattern 2's rules blindly.

**Example — Count Negative Numbers in a Sorted Matrix (matrix sorted *descending*):**
```python
class Solution:
    def countNegatives(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        row, col = 0, cols - 1   # top-right
        count = 0
        while row < rows and col >= 0:
            if grid[row][col] < 0:
                count += rows - row   # this cell + everything below it in the column
                col -= 1
            else:
                row += 1
        return count
```

`count += rows - row`: column sorted descending, so once negative, everything below is also negative — that's `rows - row` cells (current row through the last row, inclusive).

**LeetCode:** 1351 — Count Negative Numbers in a Sorted Matrix. Complexity: O(rows + cols).

---

## Pattern 5: Binary Search on Columns + Row-Max Comparison → 2D Peak

**When it applies:** matrix has NO sortedness at all. Find any cell bigger than all its neighbors (2D generalization of the 1D uphill/downhill peak trick).

**Technique:**
1. Binary search over **columns**. Pick `mid_col`.
2. Scan that entire column (O(rows)) to find the row with the max value in it — `max_row`.
3. Compare `matrix[max_row][mid_col]` to its left and right neighbors (same row).
4. Bigger than both → genuine 2D peak (guaranteed bigger than up/down too, since it was the column max).
5. Right neighbor bigger → a peak is guaranteed to exist further right (same guarantee as 1D uphill) → search right half of columns.
6. Left neighbor bigger → search left half.

```python
def findPeakGrid(mat):
    rows, cols = len(mat), len(mat[0])
    low_col, high_col = 0, cols - 1
    while low_col <= high_col:
        mid_col = (low_col + high_col) // 2
        max_row = 0
        for r in range(rows):
            if mat[r][mid_col] > mat[max_row][mid_col]:
                max_row = r
        left = mat[max_row][mid_col - 1] if mid_col > 0 else -1
        right = mat[max_row][mid_col + 1] if mid_col < cols - 1 else -1
        if mat[max_row][mid_col] > left and mat[max_row][mid_col] > right:
            return [max_row, mid_col]
        elif right > mat[max_row][mid_col]:
            low_col = mid_col + 1
        else:
            high_col = mid_col - 1
    return [-1, -1]
```

**LeetCode:** 1901 — Find a Peak Element II. Complexity: O(rows × log cols).

---

## Full Pattern Summary

| Pattern | Structure | Technique | Complexity | LeetCode |
|---|---|---|---|---|
| 1 | Fully sorted, flattenable | 1D binary search + index↔(row,col) mapping | O(log(rows×cols)) | 74 |
| 2 | Row+col sorted, not flattenable | Staircase from top-right corner | O(rows+cols) | 240 |
| 3 | Rows individually sorted only | Binary search per row | O(rows × log cols) | 1428 |
| 4 | Row+col sorted, find k-th value | Binary search on value + staircase count | O(log(range)×(rows+cols)) | 378 |
| 4b | Row+col sorted, count matches | Staircase count (direction depends on sort order) | O(rows+cols) | 1351 |
| 5 | Unsorted, find any peak | Binary search on columns + row-max + uphill/downhill | O(rows × log cols) | 1901 |

---

## Mistakes Made & Debugged During This Session

1. **`col = len(matrix)-1` instead of `len(matrix[0])-1`** — confused "number of rows" with "number of columns" when starting the staircase corner. Only surfaces on non-square matrices.
2. **Tried to apply Pattern 1 (flatten + 1D binary search) to a Pattern-4-shaped matrix (378).** Flattened row-major position is NOT the same as sorted-value rank when rows aren't globally ordered — this assumption silently gives wrong answers. Fix: must binary search on *value*, using a count subroutine, not on flattened index.
3. **Tried to invent a running-rank-counter scheme while walking row-by-row (378).** Breaks because correct ranking requires knowing about *future* rows' smaller values before finishing an earlier row — row-major traversal can't guarantee that. This is why a real k-way-merge or the count-based binary search is needed instead of a patched counter.
4. **Initialization confusion (row/col vs low/high).** Fixed with a two-question checklist:
   - Am I walking a grid (row/col, staircase-style) or searching a range (low/high, value or index)?
   - For each variable: which direction does it move, what's its start value (before any elimination), and what's the first *invalid* value in that direction (for the loop condition)?

---

## Practice List (in order)

74 → 240 → 1351 → 378 → 1901 → 1428

Full official tag list: https://leetcode.com/problem-list/binary-search/
