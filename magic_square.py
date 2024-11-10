# Problem in progress

def forming_magic_square(s):
    MAGIC_NUM = 15
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

    square_lines = [
        col_0, col_1, col_2,
        row_0, row_1, row_2,
        diag_0, diag_1]

    matrix_lines_by_idx = [
        [3, 0, 6],
        [3, 1],
        [3, 2, 7],
        [4, 0],
        [4, 1, 6, 7],
        [4, 2],
        [5, 0, 7],
        [5, 1],
        [5, 2, 6]
    ]

    def get_diffs_by_line_idxs(s_current: list[int]):
        line_diffs = [
            MAGIC_NUM - sum(
                [s_current[idx] for idx in line])
            for line in square_lines]
        
        return line_diffs
    
    diffs_by_line_idxs = get_diffs_by_line_idxs(s_flat)
    print('diffs_by_line_idxs', diffs_by_line_idxs)

    def get_diffs_by_square_idx(line_diffs: list[int]):
        idx_diffs = [[
                line_diffs[line_idx] for line_idx in lines]
            for lines in matrix_lines_by_idx]
        
        return idx_diffs

    diffs_by_idx = get_diffs_by_square_idx(diffs_by_line_idxs)
    print('diffs_by_idx', diffs_by_idx)

    def get_average_diff_by_idx(
        diff_by_idxs: list[list[int]], s_current: list[int]
    ):
        idx_average_diffs = [
            s_current[idx_diffs]
            + round(sum(line_diffs) / len(line_diffs))
            for idx_diffs, line_diffs in enumerate(diff_by_idxs)]

        return list(zip(s_current, idx_average_diffs))

    average_diff_by_idx = get_average_diff_by_idx(diffs_by_idx, s_flat)
    print('average_diff_by_idx', average_diff_by_idx)

    def get_total_diff(line_diffs: list[int]):
        return sum([abs(diff) for diff in line_diffs])
    
    total_diff = get_total_diff(diffs_by_line_idxs)
    print('total_diff', total_diff)

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
