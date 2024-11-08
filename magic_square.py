# Problem in progress
import itertools
from collections import Counter

def forming_magic_square(s):
    s_flat = [n for ng in s for n in ng]
    s_sorted = sorted(s_flat)
    print('s', s)
    print('s_flat', s_flat)

    row_0 = [0, 1, 2]
    row_1 = [3, 4, 5]
    row_2 = [6, 7, 8]
    
    col_0 = [0, 3, 6]
    col_1 = [1, 4, 7]
    col_2 = [2, 5, 8]
    
    diag_0 = [0, 4, 8]
    diag_1 = [2, 4, 6]

    matrix_groups_by_idxs = [
        [row_0, col_0, diag_0],
        [row_0, col_1],
        [row_0, col_2, diag_1],
        [row_1, col_0],
        [row_1, col_1, diag_0, diag_1],
        [row_1, col_2],
        [row_2, col_0, diag_1],
        [row_2, col_1],
        [row_2, col_2, diag_0]
    ]

    def get_missing_numbers(s_sorted):
        s_idx = 0
        num = 1
        missing_num = []
        
        while num < 10:
            if s_idx > 8 or num < s_sorted[s_idx]:
                missing_num.append(num)
                num += 1
                continue

            if num > s_sorted[s_idx]:
                s_idx += 1
                continue

            num += 1
            s_idx += 1

        return missing_num

    missing_num = get_missing_numbers(s_sorted)
    print('missing_num', missing_num)

    def get_incomplete_groups(idx_groups):
        return [
            idx_group
            for idx_group in idx_groups
            if sum([s_flat[ig] for ig in idx_group]) != 15]

    def get_repeated_idxs():
        repeated_vals = {}

        for idx, val in enumerate(s_flat):
            rest = s_flat[idx+1:]

            if val in rest or val in repeated_vals:
                if val not in repeated_vals:
                    repeated_vals[val] = [idx]
                    continue

                repeated_vals[val].append(idx)

        return repeated_vals


    return None

test_case_0 = [[4, 9, 2], [3, 5, 7], [8, 1, 5]]
test_case_0_result = 1

test_case_1 = [[4, 8, 2], [4, 5, 7], [6, 1, 6]]
test_case_1_result = 4

test_case_2 = [[4, 5, 8], [2, 4, 1], [1, 9, 7]]
test_case_2_result = 14

test_case_18 = [[6, 9, 8], [3, 9, 4], [9, 4, 4]]
test_case_18_result = 21

result = forming_magic_square(test_case_2)
print('result', result)
