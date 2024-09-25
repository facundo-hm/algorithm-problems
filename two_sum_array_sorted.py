'''
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted

Given a 1-indexed array of integers numbers that is already sorted
in non-decreasing order, find two numbers such that they add up to
a specific target number.

Return the indices of the two numbers, index1 and index2, added by
one as an integer array [index1, index2] of length 2.

Example
Input: numbers = [2, 7, 11, 15], target = 9
Output: [1, 2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1,
index2 = 2. We return [1, 2].
'''

def two_sum(numbers: list[int], target: int) -> list[int]:
    for idx, num in enumerate(numbers):
        head_idx = idx + 1
        tail_idx = len(numbers) - 1

        while tail_idx >= head_idx:
            next_idx = (head_idx + tail_idx) // 2
            curr_num = numbers[next_idx]
            curr_sum = num + curr_num

            if curr_sum == target:
                return [idx + 1, next_idx + 1]

            if curr_sum > target:
                tail_idx = next_idx - 1
                continue

            head_idx = next_idx + 1
