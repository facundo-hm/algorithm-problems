# Problem in progress
import itertools

def forming_magic_square(s):
    # Create array of indexes combinations.
    # Iterate combinations, add them and store result in a key-value map,
    # where key=sum_result and value=[[indexes], ...].
    # Iterate map and calculate which sum_result has more indexes.
    # Use the choosen sum_result to modify the rest of the indexes to
    # obtein the same sum_result with the least cost.
    
    # The sum of the combinations differences needed to reach the magic
    # constant is the final result.
    # How to obtain the magic constant, when no sum combinations have
    # the same value?
    
    s_flat = [n for ng in s for n in ng]
    s_sorted = sorted(s_flat)
    print('s', s)
    print('s_flat', s_flat)

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

    print('missing_num', missing_num)

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
    
    def is_changeable_idx(idx_groups, changeable_idxs):
        # BUG: Repeated numbers can have only some of their groups incompleted.
        # Identify them independently from this function based on some priority.

        # Check if the idx_groups are already cover
        # by the combination of previous idxs.
        incompleted_idx_groups = [
            idx_group
            for idx_group in idx_groups
            if sum([s_flat[ig] for ig in idx_group]) != 15]
        
        print('------------------------')
        print('idx_groups', idx_groups)
        print('incompleted_idx_groups', incompleted_idx_groups)

        if not len(changeable_idxs):
            return len(incompleted_idx_groups) == len(idx_groups)
        
        changeable_idx_groups = [
            group
            for idx in changeable_idxs
            for group in matrix_groups_by_idxs[idx]
        ]
        
        uncovered_groups = [
            idx_group
            for idx_group in incompleted_idx_groups
            if idx_group not in changeable_idx_groups]

        return len(incompleted_idx_groups) == len(idx_groups) and len(uncovered_groups)
        
    changeable_idxs = []
    
    for idx, idx_group in enumerate(matrix_groups_by_idxs):
        if is_changeable_idx(idx_group, changeable_idxs):
            changeable_idxs.append(idx)

    print('changeable_idxs', changeable_idxs)
    
    changeable_values = [
        s_flat[ci]
        for ci in changeable_idxs
    ]
    
    print('changeable_values', changeable_values)
    
    unique_groups = []
    
    for changeable_idx in changeable_idxs:
        ci_groups = matrix_groups_by_idxs[changeable_idx]
        new_unique_groups = [
            ci_group
            for ci_group in ci_groups
            if ci_group not in unique_groups]
        unique_groups.extend(new_unique_groups)
    
    print('unique_groups', unique_groups)
    
    ug_values_sum = sum([
        s_flat[ug_index]
        for ug_indexes in unique_groups
        for ug_index in ug_indexes
    ])
    
    print('ug_values_sum', ug_values_sum)
    
    ug_final_value = 15 * len(unique_groups)
    
    print('ug_final_value', ug_final_value)
    
    ug_difference = ug_final_value - ug_values_sum
    
    print('ug_difference', ug_difference)
    
    ci_total_value = sum([
        s_flat[ci] * len(matrix_groups_by_idxs[ci])
        for ci in changeable_idxs
    ])
    
    print('ci_total_value', ci_total_value)
    
    current_remainder = ug_values_sum - ci_total_value
    
    print('current_remainder', current_remainder)
    
    final_value_without_remainder = ug_final_value - current_remainder
    
    print('value to get', final_value_without_remainder)

    new_values_diff = abs(len(missing_num) - len(changeable_values))
    new_values = ([
        [*missing_num, *changeable_values[n:n+new_values_diff]]
        for n in range(0, len(changeable_values), new_values_diff)]
        if len(missing_num)
        else changeable_values)
    
    print('new_values', new_values)

    total_diff_sum = float('inf')

    for new_value in new_values:
        for nv_permutation in itertools.permutations(new_value, len(new_value)):
            permutation_sum = sum([
                nv_permutation[idx] * len(matrix_groups_by_idxs[c_idx])
                for idx, c_idx in enumerate(changeable_idxs)])
            
            if permutation_sum == final_value_without_remainder:
                differences = [
                    abs(matched_values[0] - matched_values[1])
                    for matched_values
                    in zip(nv_permutation, changeable_values)]
                differences_sum = sum(differences)

                if differences_sum < total_diff_sum:
                    total_diff_sum = differences_sum

                print('----------')
                print('differences', differences)
                print('differences_sum', differences_sum)
                print('permutation_sum', permutation_sum)
                print('nv_permutation', nv_permutation)
    
    # Identify indexes that have to be changed by checking
    # that all each of its gorups doesn't add up to 15.
    
    # If there is no missing numbers, try by switching indexes
    # that have to be changed.
    
    # Compute the value to achieve with the new numbers combination.
    # Add the values of all lines.
    # 14+14+14+16+13+13 = 84
    # Compute the lines total final value.
    # 15*6 = 90
    # Difference between final and current total values.
    # 90-84 = 6
    # Total value of the number to be changed.
    # 8*2+4*2+6*3 = 42
    # Total value of the new numbers.
    # 9*2+3*2+8*3 = 48
    # Current remainder without the number to be changed total value.
    # 84-42 = 42
    # Final tota value without current reminder
    # 90-42 = 48
    # Difference between total values of new numbers and number to be changed.
    # 48-42 = 6
    
    return total_diff_sum


test_case_1 = [[4, 5, 8], [2, 4, 1], [1, 9, 7]]
test_case_1_result = 14

test_case_18 = [[6, 9, 8], [3, 9, 4], [9, 4, 4]]
test_case_18_result = 21

result = forming_magic_square(test_case_1)
print('result', result)
