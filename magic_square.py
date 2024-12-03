# Problem in progress
from math import ceil

def forming_magic_square(s: list[list[int]]):
    MAGIC_NUM = 15
    MAX_VAL = 10
    MIN_VAL = 0
    MAX_DEPTH = 5
    SWITCH_SUMS = 0

    s_flat = [n for ng in s for n in ng]

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

    def get_missing_numbers(s_flat: list[int]):
        s_sorted = sorted(s_flat)
        s_idx = 0
        num = 1
        missing_num: list[int] = []
        
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

    def get_diffs_by_line_idxs(s_current: list[int]):
        line_diffs = [
            sum([s_current[idx] for idx in line])
            for line in square_lines]
        
        return line_diffs

    def get_diffs_by_square_idx(line_diffs: list[int]):
        idx_diffs = [[
                line_diffs[line_idx] for line_idx in lines]
            for lines in matrix_lines_by_idx]
        
        return idx_diffs

    def get_idx_diff_pairs(
        diffs_by_line_idxs: list[int],
        s_current: list[int],
        last_seen: list[int] = []
    ):
        diff_by_idxs = get_diffs_by_square_idx(diffs_by_line_idxs)
        print('diffs_by_line_idxs', diffs_by_line_idxs)
        # print('diff_by_idxs', diff_by_idxs)

        idx_diff_lines = set()

        for idx_diffs, line_diffs in enumerate(diff_by_idxs):
            line_diffs_sum = sum(line_diffs)
            line_diffs_remainder = (
                (len(line_diffs) * MAGIC_NUM) - line_diffs_sum)
            line_diffs_ave = (
                line_diffs_remainder
                if abs(line_diffs_remainder) < len(line_diffs)
                else ceil(line_diffs_remainder / len(line_diffs)))
            idx_diff_val = s_current[idx_diffs] + line_diffs_ave
            
            if (
                idx_diffs in last_seen
                or idx_diff_val == s_current[idx_diffs]
                or idx_diff_val <= MIN_VAL or idx_diff_val >= MAX_VAL
            ):
                continue
            
            idx_diff_lines.add((idx_diffs, idx_diff_val))

        sorted_idx_diff_lines = sorted(
            list(idx_diff_lines),
            key=lambda pair: (abs(s_current[pair[0]] - pair[1])))

        return sorted_idx_diff_lines
        # return idx_diff_lines
    
    def get_total_diff(line_diffs: list[int]):
        return sum([abs(diff - MAGIC_NUM) for diff in line_diffs])

    def get_next_s(
        switch_items: tuple[int, int],
        s_current: list[int]
    ):
        remove_item_idx, add_item_val = (switch_items[0], switch_items[1])
        s_new = s_current[:]
        s_new[remove_item_idx] = add_item_val

        return s_new

    def update_square(
        s_current: list[int] = [],
        switch_diffs: int = SWITCH_SUMS,
        last_seen: list[int] = [],
        max_depth: int = MAX_DEPTH
    ):
        print('------------------')
        print('s_current', s_current)
        print('max_depth', max_depth)

        initial_diffs_by_line_idxs = get_diffs_by_line_idxs(s_current)
        initial_total_sum_diffs = get_total_diff(initial_diffs_by_line_idxs)
        initial_idx_diff_pairs = get_idx_diff_pairs(
            initial_diffs_by_line_idxs, s_current, last_seen)
        
        print('initial_total_sum_diffs', initial_total_sum_diffs)
        print('initial_idx_diff_pairs', initial_idx_diff_pairs)

        if (
            initial_total_sum_diffs == 0
            or max_depth == 0 or
            not len(initial_idx_diff_pairs)
        ):
            missing_numbers = get_missing_numbers(s_current)
            return (
                None
                if (
                    initial_total_sum_diffs > 0
                    or (initial_total_sum_diffs == 0 and len(missing_numbers)))
                else switch_diffs)

        least_diff_val: int = float('inf')

        for idx_diff_pair in initial_idx_diff_pairs:
            remove_item_idx: int = idx_diff_pair[0]
            remove_item_diff: int = idx_diff_pair[1]
            remove_item_val: int = s_current[remove_item_idx]

            switch_diff = abs(remove_item_val - remove_item_diff)
            next_switch = (remove_item_idx, remove_item_diff)
            s_new = get_next_s(next_switch, s_current)

            curr_path_result = update_square(
                s_new, switch_diff, [remove_item_idx], max_depth - 1)

            print(f'**Next Result** {curr_path_result}')

            if (
                curr_path_result != None
                and curr_path_result < least_diff_val
            ):
                least_diff_val = curr_path_result

        new_switch_diffs = least_diff_val + switch_diffs

        print(
            f'max_depth: {max_depth}, new_switch_diffs: {new_switch_diffs}')

        return new_switch_diffs

    return update_square(s_flat, SWITCH_SUMS, max_depth=MAX_DEPTH)

test_case_0 = [[4, 9, 2], [3, 5, 7], [8, 1, 5]]
test_case_0_result = 1

test_case_0b = [[5, 3, 4], [1, 5, 8], [6, 4, 2]]
test_case_0b_result = 7

test_case_1 = [[4, 8, 2], [4, 5, 7], [6, 1, 6]]
test_case_1_result = 4

test_case_2 = [[4, 5, 8], [2, 4, 1], [1, 9, 7]]
test_case_2_result = 14

test_case_18 = [[6, 9, 8], [3, 9, 4], [9, 4, 4]]
test_case_18_result = 21

result = forming_magic_square(test_case_1)
print('result', result)
