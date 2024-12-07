# Problem in progress
from math import ceil

def forming_magic_square(s: list[list[int]]):
    MAGIC_NUM = 15
    MAX_VAL = 10
    MIN_VAL = 0
    MAX_DEPTH = 10
    SWITCH_SUMS = float('inf')

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
        print('diff_by_idxs', diff_by_idxs)

        idx_diff_lines = set()

        for idx_diffs, line_diffs in enumerate(diff_by_idxs):
            idx_val = s_current[idx_diffs]

            # if MAGIC_NUM in line_diffs or idx_diffs in last_seen:
            if idx_diffs in last_seen:
                continue
            
            diff_vals = [
                idx_val + (MAGIC_NUM - line_diff)
                for line_diff in line_diffs
                if line_diff != MAGIC_NUM
            ]

            idx_diff_vals = [
                (idx_diffs, diff_val)
                for diff_val in diff_vals
                if diff_val != idx_val
                and diff_val > MIN_VAL
                and diff_val < MAX_VAL
            ]

            idx_diff_lines.update(idx_diff_vals)

        sorted_idx_diff_lines = sorted(
            list(idx_diff_lines),
            key=lambda pair: (abs(s_current[pair[0]] - pair[1])))

        # return sorted_idx_diff_lines
        return idx_diff_lines
    
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

    def get_path_result(
        idx_diff_pair: tuple[int, int],
        s_current: list[int],
        least_switch_diffs: int,
        prev_switch_diffs: int,
        last_seen: list[int]
    ):
        remove_item_idx: int = idx_diff_pair[0]
        remove_item_diff: int = idx_diff_pair[1]
        remove_item_val: int = s_current[remove_item_idx]

        switch_diff = abs(remove_item_val - remove_item_diff)
        next_switch = (remove_item_idx, remove_item_diff)
        s_new = get_next_s(next_switch, s_current)

        new_last_seen = last_seen[:]
        new_last_seen.append(remove_item_idx)

    def update_square(
        s_current: list[int] = [],
        least_switch_diffs: int = SWITCH_SUMS,
        prev_switch_diffs: int = 0,
        last_seen: list[int] = [],
        max_depth: int = MAX_DEPTH,
        main_call: bool = True
    ):
        print('------------------')
        print('s_current', s_current)
        print('max_depth', max_depth)
        print('last_seen', last_seen)
        print('least_switch_diffs', least_switch_diffs)
        print('prev_switch_diffs', prev_switch_diffs)

        diffs_by_line_idxs = get_diffs_by_line_idxs(s_current)
        total_sum_diffs = get_total_diff(diffs_by_line_idxs)
        idx_diff_pairs = get_idx_diff_pairs(
            diffs_by_line_idxs, s_current, last_seen)
        
        print('total_sum_diffs', total_sum_diffs)
        print('idx_diff_pairs', idx_diff_pairs)

        if (
            total_sum_diffs == 0
            or max_depth == 0 or
            not len(idx_diff_pairs)
        ):
            print('<-- base case return')
            missing_numbers = get_missing_numbers(s_current)
            return (
                float('inf')
                if total_sum_diffs > 0 or len(missing_numbers)
                else prev_switch_diffs)

        least_diff_val: int = float('inf')
        least_total_val: int = float('inf')
        least_s: list[int] = []
        least_last_seen: list[int] = []

        for idx_diff_pair in idx_diff_pairs:
            print('....')
            print('idx_diff_pair', idx_diff_pair)
            remove_item_idx: int = idx_diff_pair[0]
            remove_item_diff: int = idx_diff_pair[1]
            remove_item_val: int = s_current[remove_item_idx]

            switch_diff = abs(remove_item_val - remove_item_diff)
            next_switch = (remove_item_idx, remove_item_diff)
            s_new = get_next_s(next_switch, s_current)
            print('s_new', s_new)
            local_diffs_by_line_idxs = get_diffs_by_line_idxs(s_new)
            local_total_sum_diffs = get_total_diff(local_diffs_by_line_idxs)

            new_last_seen = [remove_item_idx]

            curr_path_result = prev_switch_diffs

            if main_call:
                curr_path_result = update_square(
                    s_new, least_switch_diffs, 0,
                    new_last_seen, max_depth - 1, False)

            switch_diff = switch_diff + curr_path_result
            print(f'**{idx_diff_pair}** {main_call}, {curr_path_result}, {switch_diff}, {local_total_sum_diffs}')

            if local_total_sum_diffs < least_total_val:
                least_diff_val = switch_diff
                least_s = s_new
                least_last_seen = new_last_seen
                least_total_val = local_total_sum_diffs

        print(
            f'least_diff_val: {least_diff_val}, least_s {least_s}, least_last_seen {least_last_seen}')

        if main_call:
            print('<- main case return')
            return least_diff_val

        return update_square(
            least_s, least_switch_diffs, least_diff_val,
            least_last_seen, max_depth - 1, False)

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

result = forming_magic_square(test_case_2)
print('result', result)
