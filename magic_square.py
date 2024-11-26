# Problem in progress

def forming_magic_square(s: list[list[int]]):
    MAGIC_NUM = 15
    MAX_DEPTH = 5

    s_flat = [n for ng in s for n in ng]
    s_sorted = sorted(s_flat)
    print('s', s)
    print('s_flat', s_flat)

    global total_sum_diffs
    global switch_diffs
    total_sum_diffs = 0
    switch_diffs = 0

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

    def get_missing_numbers(s_sorted):
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

    def get_repeated_vals():
        repeated_vals = []

        for idx, val in enumerate(s_flat):
            rest = s_flat[idx+1:]

            if val in rest:
                repeated_vals.append(val)

        return repeated_vals

    missing_num = get_missing_numbers(s_sorted)
    print('missing_num', missing_num)

    repeated_vals = get_repeated_vals()
    print('repeated_vals', repeated_vals)

    def get_diffs_by_line_idxs(s_current: list[int]):
        line_diffs = [
            MAGIC_NUM - sum(
                [s_current[idx] for idx in line])
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
        last_seen: int = None
    ):
        diff_by_idxs = get_diffs_by_square_idx(diffs_by_line_idxs)
        # print('diff_by_idxs', diff_by_idxs)
        
        idx_diff_lines = {
            (idx_diffs, s_current[idx_diffs] + line_diff)
            for idx_diffs, line_diffs in enumerate(diff_by_idxs)
            for line_diff in line_diffs
            if (
                idx_diffs != last_seen and
                (s_current[idx_diffs] + line_diff) != s_current[idx_diffs]
                and (s_current[idx_diffs] + line_diff) > 0 and
                (s_current[idx_diffs] + line_diff) < 10)}
        # print('idx_diff_lines', idx_diff_lines)

        sorted_idx_diff_lines = sorted(
            list(idx_diff_lines),
            key=lambda pair: (
                pair[1] not in missing_num,
                s_current[pair[0]] not in repeated_vals,
                abs(s_current[pair[0]] - pair[1])))

        # return sorted_idx_diff_lines
        return idx_diff_lines
    
    def get_total_diff(line_diffs: list[int]):
        return sum([abs(diff) for diff in line_diffs])

    def get_next_s(
        switch_items: tuple[int, int],
        s_current: list[int]
    ):
        remove_item_idx, add_item_val = (switch_items[0], switch_items[1])
        s_new = s_current[:]
        s_new[remove_item_idx] = add_item_val

        return s_new

    def update_square(
        idx_diff_pairs: list[tuple[int, int]],
        s_current: list[int],
        max_depth: int
    ):
        global total_sum_diffs
        global switch_diffs

        print('------------------')
        print(f'missing_num: {missing_num}, repeated_vals: {repeated_vals}')
        print('s_current', s_current)
        print('idx_diff_pairs', idx_diff_pairs)

        if (total_sum_diffs == 0 or max_depth == 0):
            return switch_diffs

        least_diff_switch = None
        least_total_sum = float('inf')
        least_diff_val: int
        least_diff_sum: int
        s_final: list[int]
        diffs_by_line_idxs: list[int]

        for idx_diff_pair in idx_diff_pairs:
            remove_item_idx: int = idx_diff_pair[0]
            remove_item_diff: int = idx_diff_pair[1]
            remove_item_val: int = s_current[remove_item_idx]

            if (
                remove_item_diff not in missing_num
                and remove_item_diff not in s_current
            ):
                continue

            switch_diff = abs(remove_item_val - remove_item_diff)
            next_switch = (remove_item_idx, remove_item_diff)
            s_new = get_next_s(next_switch, s_current)
            new_diffs_by_line_idxs = get_diffs_by_line_idxs(s_new)
            new_total_sum_diffs = get_total_diff(new_diffs_by_line_idxs)
            new_total_sum = new_total_sum_diffs + switch_diff

            print(f'next_switch {next_switch}, new_total_sum {new_total_sum}')

            # this condition is not consider the case where a greater total_sum
            # is bet on the sake of future better result.
            if (
                new_total_sum < least_total_sum
            ):
                least_diff_sum = new_total_sum_diffs
                least_diff_val = switch_diff
                least_total_sum = new_total_sum
                least_diff_switch = next_switch
                s_final = s_new
                diffs_by_line_idxs = new_diffs_by_line_idxs

        print(f'least_diff_switch {least_diff_switch}, least_total_sum {least_total_sum}')

        if not least_diff_switch:
            return switch_diffs

        remove_item_idx, add_item_val = least_diff_switch[0], least_diff_switch[1]
        remove_item_val: int = s_current[remove_item_idx]

        new_idx_diff_pairs = get_idx_diff_pairs(
            diffs_by_line_idxs, s_final, remove_item_idx)

        if least_diff_sum >= total_sum_diffs:
            max_depth -= 1

        total_sum_diffs = least_diff_sum
        switch_diffs += least_diff_val

        print(
            f'max_depth: {max_depth}, switch_diffs: {switch_diffs}, total_sum_diffs: {total_sum_diffs}')

        if add_item_val in missing_num:
            missing_num.remove(add_item_val)

            if remove_item_val not in repeated_vals:
                missing_num.append(remove_item_val)
            else:
                repeated_vals.remove(remove_item_val)
        else:
            if remove_item_val in repeated_vals:
                repeated_vals.remove(remove_item_val)
            else:
                missing_num.append(remove_item_val)

            repeated_vals.append(add_item_val)

        return update_square(new_idx_diff_pairs, s_final, max_depth)

    initial_diffs_by_line_idxs = get_diffs_by_line_idxs(s_flat)
    initial_idx_diff_pairs = get_idx_diff_pairs(
        initial_diffs_by_line_idxs, s_flat, [])
    initial_total_sum_diffs = get_total_diff(initial_diffs_by_line_idxs)

    print('initial_diffs_by_line_idxs', initial_diffs_by_line_idxs)
    print('initial_idx_diff_pairs', initial_idx_diff_pairs)
    print('initial_total_diff', initial_total_sum_diffs)

    final_result = float('inf')

    for idx_diff_pair in initial_idx_diff_pairs:
        print('*************************************')

        total_sum_diffs = initial_total_sum_diffs
        switch_diffs = 0
        missing_num = get_missing_numbers(s_sorted)
        repeated_vals = get_repeated_vals()
        
        print('initial_idx_diff_pairs', initial_idx_diff_pairs)
        print('next_idx_diff_pairs', idx_diff_pair)

        result = update_square([idx_diff_pair], s_flat, MAX_DEPTH)

        if (
            result < final_result
            and total_sum_diffs == 0
            and not len(missing_num)
            and not len(repeated_vals)
        ):
            final_result = result

        print('\nresult', result)
        print('final_result', final_result)
        print('total_sum_diffs', total_sum_diffs)
        print('missing_num', missing_num)
        print('repeated_vals', repeated_vals)

    return final_result

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

result = forming_magic_square(test_case_18)
print('result', result)
