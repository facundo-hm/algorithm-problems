# Problem in progress
import itertools
import math

def forming_magic_square(s):
    # Create array of indexes combinations.
    # Iterate combinations, add them and store result in a key-value map,
    # where key=sum_result and value=[[indexes], ...].
    # Iterate map and calculate which sum_result has more indexes.
    # Use the choosen sum_result to modify the rest of the indexes to
    # obtain the same sum_result with the least cost.
    
    # The sum of the combinations differences needed to reach the magic
    # constant is the final result.
    # How to obtain the magic constant, when no sum combinations have
    # the same value?
    
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

    all_matrix_groups = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
        [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    
    all_matrix_groups_sum = [
        sum([s_flat[mg_idx] for mg_idx in mg])
        for mg in all_matrix_groups
    ]

    print('all_matrix_groups_sum', all_matrix_groups_sum)
    print('all_matrix_groups_total_sum', sum(all_matrix_groups_sum))

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
    
    def combine_repeated_idxs(repeated_vals_idxs: list[list[int]]):
        repeated_idxs_combination = [
            list(itertools.combinations(
                repeated_val_idxs, len(repeated_val_idxs) - 1))
            for repeated_val_idxs in repeated_vals_idxs]
        
        repeated_idxs_product = [[
                idx 
                for product in products
                for idx in product]
            for products in itertools.product(*repeated_idxs_combination)]

        return repeated_idxs_product

    repeated_idxs = get_repeated_idxs()
    # print('repeated_idxs', repeated_idxs)

    repeated_idxs_values = [
        values for values in repeated_idxs.values()]
    repeated_idxs_combination = combine_repeated_idxs(repeated_idxs_values)
    print('repeated_idxs_combination', repeated_idxs_combination)

    def is_changeable_idx(idx_groups, changeable_idxs):
        incomplete_idx_groups = get_incomplete_groups(idx_group)

        if len(incomplete_idx_groups) == len(idx_groups):
            if not len(changeable_idxs):
                return True

            # Check if the idx_groups are already cover
            # by the combination of previous idxs.        
            changeable_idx_groups = [
                group
                for idx in changeable_idxs
                for group in matrix_groups_by_idxs[idx]
            ]
            
            uncovered_groups = [
                idx_group
                for idx_group in incomplete_idx_groups
                if idx_group not in changeable_idx_groups]

            return bool(uncovered_groups)
        
        return False

    missing_num = get_missing_numbers(s_sorted)
    print('missing_num', missing_num)

    changeable_idxs_combination: list[list] = []

    for ric in repeated_idxs_combination:
        changeable_idxs = ric[:]

        for idx, idx_group in enumerate(matrix_groups_by_idxs):
            if is_changeable_idx(idx_group, changeable_idxs):
                changeable_idxs.append(idx)

        changeable_idxs_combination.append(changeable_idxs)

    print('changeable_idxs_combination', changeable_idxs_combination)

    unique_changeable_idxs = list({
        idx for idxs in changeable_idxs_combination for idx in idxs})
    
    print('unique_changeable_idxs', unique_changeable_idxs)

    changeable_values_combination = [
        [s_flat[ci] for ci in cic]
        for cic in changeable_idxs_combination
    ]

    print('changeable_values_combination', changeable_values_combination)

    unique_changeable_values = list({
        val for vals in changeable_values_combination for val in vals})
    
    print('unique_changeable_values', unique_changeable_values)

    unique_groups = []
    
    for changeable_idx in unique_changeable_idxs:
        ci_groups = matrix_groups_by_idxs[changeable_idx]
        new_unique_groups = [
            ci_group
            for ci_group in ci_groups
            if ci_group not in unique_groups and sum(
                [s_flat[idx] for idx in ci_group]) != 15]
            # if ci_group not in unique_groups]
        unique_groups.extend(new_unique_groups)
    
    print('unique_groups', unique_groups)

    new_values_combinations_diff = abs(len(missing_num) - len(
        max(changeable_idxs_combination, key=len)))
    new_values_combinations = ([
        [*missing_num, *n]
        for n in itertools.combinations(
            unique_changeable_values, new_values_combinations_diff)]
        if len(missing_num)
        else unique_changeable_values)
    
    print('new_values_combinations', new_values_combinations)

    unique_group_by_changeable_idx = {
        changeable_idx: [
            unique_group
            for unique_group in unique_groups
            if changeable_idx in unique_group]
        for changeable_idx in unique_changeable_idxs}
    
    print('unique_group_by_changeable_idx', unique_group_by_changeable_idx)

    total_diff_sum = float('inf')
    nv_permutations = [
        nvp
        for nvc in new_values_combinations
        for nvp in itertools.permutations(nvc, len(nvc))]

    for cic in changeable_idxs_combination:
        groups_by_cic = [
            unique_group_by_changeable_idx[ci]
            for ci in cic
        ]

        for nvp in nv_permutations:
            permutations_by_changeable_idx = {
                ci: nvp[idx]
                for idx, ci in enumerate(cic)}
            cvc = [s_flat[ci] for ci in cic]

            unique_group_by_changeable_idx_sum = sum([sum([
                    sum([
                        permutations_by_changeable_idx[ug_idx]
                        if ug_idx in permutations_by_changeable_idx
                        else s_flat[ug_idx]
                        for ug_idx in unique_group_ci])
                    for unique_group_ci in unique_groups_ci]) / len(unique_groups_ci)
                for unique_groups_ci in groups_by_cic]) // len(groups_by_cic)

            unique_groups_sums = []

            for unique_group in unique_groups:
                unique_group_values = [
                    permutations_by_changeable_idx[ug_idx]
                    if ug_idx in permutations_by_changeable_idx
                    else s_flat[ug_idx]
                    for ug_idx in unique_group
                ]
                unique_group_sum = sum(unique_group_values)
                unique_groups_sums.append(unique_group_sum)

            unique_groups_total_sum = sum(unique_groups_sums)
            unique_groups_total_ave = (
                unique_groups_total_sum / len(unique_groups_sums))

            if (unique_groups_total_ave != 15):
                continue

            # if (
            #     unique_groups_total_ave != 15
            #     or math.floor(unique_group_by_changeable_idx_sum) != 15
            # ):
            #     continue

            # if round(unique_group_by_changeable_idx_sum) != 15:
            #     continue

            differences = [
                abs(matched_values[0] - matched_values[1])
                for matched_values in zip(nvp, cvc)
                if matched_values[0] != matched_values[1]]
            
            if len(differences) != len(cvc):
                continue

            differences_sum = sum(differences)

            if differences_sum < total_diff_sum:
                total_diff_sum = differences_sum

            print('------------------------------')
            print('nvp', nvp)
            print('cvc', cvc)
            print('differences', differences)
            print('unique_group_by_changeable_idx_sum', unique_group_by_changeable_idx_sum)
            print('differences_sum', differences_sum)
            print('unique_groups_total_ave', unique_groups_total_ave)

    '''
    Identify indexes that have to be changed by checking
    that all each of its gorups doesn't add up to 15.
    
    If there is no missing numbers, try by switching indexes
    that have to be changed.
    
    Compute the value to achieve with the new numbers combination.
    [[4, 8, 2], [4, 5, 7], [6, 1, 6]]
    - Add the values of all uinique lines.
    14 + 14 + 14 + 16 + 13 + 13 = 84
    - Compute the lines total final value.
    15*6 = 90
    - Difference between final and current total values.
    90 - 84 = 6
    - Total value of the numbers to be changed, where each one
    is multiplied by the times that appears in each unique line.
    8*2 + 4*2 + 6*3 = 42
    - Total value of the new numbers after being placed in
    the square idx.
    9*2 + 3*2 + 8*3 = 48
    - Remainder of the current total value without the numbers
    to be changed total value.
    84 - 42 = 42
    - Final total value without current remainder.
    90 - 42 = 48
    - Difference between total values of new numbers and
    number to be changed.
    48 - 42 = 6
    '''
    
    return total_diff_sum

test_case_0 = [[4, 9, 2], [3, 5, 7], [8, 1, 5]]
test_case_0_result = 1

test_case_1 = [[4, 8, 2], [4, 5, 7], [6, 1, 6]]
test_case_1_result = 4

test_case_2 = [[4, 5, 8], [2, 4, 1], [1, 9, 7]]
test_case_2_result = 14

test_case_18 = [[6, 9, 8], [3, 9, 4], [9, 4, 4]]
test_case_18_result = 21

'''
9, 9, 4, 9, 4, 4
1, 2, 5, 7

When there are repeated values, the changeable values
should consider all of them as possibilities to be changed.

An array for each varian with n-1 of each reapeted value.
Where n = total of value repeatitions.
'''

result = forming_magic_square(test_case_18)
print('result', result)
