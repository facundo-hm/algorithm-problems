# Problem in progress
import itertools

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
                    repeated_vals[val] = idx
                    continue

                prev_idx_groups = matrix_groups_by_idxs[
                    repeated_vals[val]]
                prev_incomplete_groups = get_incomplete_groups(
                    prev_idx_groups)

                curr_idx_groups = matrix_groups_by_idxs[idx]
                curr_incomplete_groups = get_incomplete_groups(
                    curr_idx_groups)

                if curr_incomplete_groups > prev_incomplete_groups:
                    repeated_vals[val] = idx

        return repeated_vals

    repeated_idxs = get_repeated_idxs()
    print('repeated_idxs', repeated_idxs)

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

    changeable_idxs = list(repeated_idxs.values())
    # changeable_idxs = [6, 8]
    
    for idx, idx_group in enumerate(matrix_groups_by_idxs):
        if is_changeable_idx(idx_group, changeable_idxs):
            changeable_idxs.append(idx)

    print('changeable_idxs', changeable_idxs)
    
    changeable_values = [
        s_flat[ci]
        for ci in changeable_idxs
    ]
    
    print('changeable_values', changeable_values)
    
    unique_groups = [
        group
        for changeable_idx in changeable_idxs
        for group in matrix_groups_by_idxs[changeable_idx]]
    # unique_groups = []
    
    # for changeable_idx in changeable_idxs:
    #     ci_groups = matrix_groups_by_idxs[changeable_idx]
    #     new_unique_groups = [
    #         ci_group
    #         for ci_group in ci_groups
    #         # if ci_group not in unique_groups and sum(
    #         #     [s_flat[idx] for idx in ci_group]) != 15]
    #         if ci_group not in unique_groups]
    #     unique_groups.extend(new_unique_groups)
    
    print('unique_groups', unique_groups)

    new_values_diff = abs(len(missing_num) - len(changeable_values))
    new_values = ([
        [*missing_num, *n]
        for n in itertools.combinations(
            changeable_values, new_values_diff)]
        if len(missing_num)
        else changeable_values)
    
    print('new_values', new_values)

    total_diff_sum = float('inf')

    for new_value in new_values:
        for nv_permutation in itertools.permutations(
            new_value, len(new_value)
        ):
            unique_groups_copy = unique_groups[:]
            permutations_by_changeable_idx = {
                ci: nv_permutation[idx]
                for idx, ci in enumerate(changeable_idxs)}

            unique_groups_sums = []

            for unique_group in unique_groups_copy:
                unique_group_values = [
                    permutations_by_changeable_idx[ug_idx]
                    if ug_idx in changeable_idxs
                    else s_flat[ug_idx]
                    for ug_idx in unique_group
                ]
                unique_group_sum = sum(unique_group_values)
                unique_groups_sums.append(unique_group_sum)

            unique_groups_total_sum = sum(unique_groups_sums)

            if unique_groups_total_sum / len(unique_groups_sums) != 15:
                continue

            differences = [
                abs(matched_values[0] - matched_values[1])
                for matched_values
                in zip(nv_permutation, changeable_values)
                if matched_values[0] != matched_values[1]]
            
            if len(differences) != len(changeable_values):
                continue

            differences_sum = sum(differences)

            if differences_sum < total_diff_sum:
                total_diff_sum = differences_sum

            print('----------')
            print('unique_groups_sums', unique_groups_sums)
            print('differences', differences)
            print('differences_sum', differences_sum)
            print('nv_permutation', nv_permutation)
            print('changeable_values', changeable_values)

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

result = forming_magic_square(test_case_18)
print('result', result)


# [[3, 4, 5], [0, 3, 6], [6, 7, 8], [2, 4, 6], [0, 1, 2], [1, 4, 7]]
# [3, 6, 1]
