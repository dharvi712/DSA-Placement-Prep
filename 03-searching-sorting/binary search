Almost every binary search variant is one of these four shapes. Memorize the shape, not the code — the code falls out once you understand which shape you need.
Template A — Exact match (what you already have)
python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
Range is inclusive [left, right]. Loop continues while left <= right.
Template B — Leftmost/rightmost boundary (lower_bound / upper_bound)
python
def lower_bound(arr, target):
    # first index where arr[index] >= target
    left, right = 0, len(arr)          # note: right = len(arr), NOT len(arr)-1
    while left < right:                # note: strict 
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid                # not mid - 1
    return left
python
def upper_bound(arr, target):
    # first index where arr[index] > target
    left, right = 0, len(arr)
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left
This is the template most people get wrong, so let's be precise about why it looks different from Template A:
We search on a half-open range [left, right), not inclusive. That's why right starts at len(arr), not len(arr)-1.
Loop condition is left < right — when left == right, the range is empty, so we're done.
We never do right = mid - 1. We do right = mid, because mid itself might still be the answer (it's a valid candidate, we just haven't ruled it out).
The answer is left when the loop ends (left == right at that point).
lower_bound and upper_bound immediately give you:
First occurrence of target = lower_bound(arr, target), if arr[that index] == target, else target isn't present.
Last occurrence of target = upper_bound(arr, target) - 1, if valid.
Count of target in sorted array = upper_bound(arr, target) - lower_bound(arr, target).
Template C — Binary search on the answer (parametric search)
Used when you're not searching an array directly, but searching over a range of possible answers, using a monotonic predicate (is_feasible(x) is False...False True...True or vice versa).
python
def binary_search_on_answer(low, high, is_feasible):
    while low < high:
        mid = low + (high - low) // 2
        if is_feasible(mid):
            high = mid       # mid works, try to do better
        else:
            low = mid + 1    # mid doesn't work, need more
    return low
Classic examples: "minimum capacity to ship packages within D days," "smallest divisor such that sum of divisions ≤ threshold," "Koko eating bananas," "square root of x." The key skill isn't the binary search loop (always the same) — it's proving the predicate is monotonic and writing is_feasible.
Template D — Binary search on a rotated / non-standard sorted array
Here the trick is: at every step, at least one half of [left, mid] or [mid, right] is guaranteed to be normally sorted. Identify which half is sorted, then check if the target lies in that sorted half's range.
python
def search_rotated(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid

        if arr[left] <= arr[mid]:          # left half is sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:                               # right half is sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
Trace this once on [4,5,6,7,0,1,2], target = 0:
left	right	mid	arr[mid]	which half sorted?	is target in it?	action
0	6	3	7	arr[0]=4 <= arr[3]=7 → left sorted	is 4<=0<7? No	left = mid+1 = 4
4	6	5	1	arr[4]=0 <= arr[5]=1 → left sorted	is 0<=0<1? Yes	right = mid-1 = 4
4	4	4	0	—	arr[mid]==target	return 4
1.4 Other must-know binary search variants
Find peak element (element greater than both neighbors, array not sorted globally): compare arr[mid] to arr[mid+1]; if increasing, peak is to the right; else peak is to the left or at mid. Same skeleton as Template B.
Search in a 2D sorted matrix: treat the matrix as a flattened sorted array; convert mid to (row, col) via divmod(mid, num_cols).
Median of two sorted arrays (hard, O(log(min(m,n)))): binary search on the partition point of the smaller array, not on values.
Allocate minimum pages / split array largest sum: Template C in disguise — binary search on the answer (max sum per partition), with is_feasible = "can I split into ≤k parts each ≤ this sum."
1.5 Complexity
Binary search: O(log n) time, O(1) space (iterative) or O(log n) space (recursive, due to call stack). This connects directly to what you flagged from Day 1: halving the search space with O(1) work per step gives the recurrence T(n) = T(n/2) + O(1), which solves to O(log n) by the Master Theorem (case 2).
