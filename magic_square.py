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
        seen_vals: list[tuple[int, int]] = []
    ):
        diff_by_idxs = get_diffs_by_square_idx(diffs_by_line_idxs)
        print('diff_by_idxs', diff_by_idxs)

        last_seen = seen_vals[-1][0] if len(seen_vals) else None
        
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

        return sorted_idx_diff_lines
    
    def get_total_diff(line_diffs: list[int]):
        return sum([abs(diff) for diff in line_diffs])

    def get_next_switch(
        idx_diff_pairs: list[tuple[int, int]], s_current:list[int]
    ):
        least_diff_switch = None
        least_diff_val = float('inf')
        least_diff_sum = float('inf')

        for idx_diff_pair in idx_diff_pairs:
            first_item_idx: int = idx_diff_pair[0]
            first_item_diff: int = idx_diff_pair[1]

            if (
                first_item_diff not in missing_num
                and first_item_diff not in s_current
            ):
                continue

            remove_item = first_item_idx, s_current[first_item_idx]
            add_item_idx = (
                None if first_item_diff in missing_num
                # it could have the same val in different idxs
                else s_current.index(first_item_diff))
            add_item = add_item_idx, first_item_diff
            switch_diff = abs(remove_item[1] - add_item[1])
            next_switch = remove_item, add_item

            s_new = get_next_s(next_switch, s_current)
            new_diffs_by_line_idxs = get_diffs_by_line_idxs(s_new)
            new_total_sum_diffs = get_total_diff(new_diffs_by_line_idxs)

            # this condition is not consider the case where a greater total_sum
            # is bet on the sake of future better result.
            if (
                new_total_sum_diffs < least_diff_sum
                and switch_diff <= least_diff_val
            ):
                least_diff_sum = new_total_sum_diffs
                least_diff_val = switch_diff
                least_diff_switch = next_switch
            
            print(f'least_diff_switch {least_diff_switch}, least_diff_val {least_diff_val}, least_diff_sum {least_diff_sum}')

        return least_diff_switch

    def get_next_s(
        switch_items: tuple[tuple[int, int]],
        s_current: list[int]
    ):
        add_item, remove_item = switch_items[1], switch_items[0]
        add_item_val = add_item[1]
        remove_item_idx = remove_item[0]

        s_new = s_current[:]
        s_new[remove_item_idx] = add_item_val

        return s_new

    def update_square(
        idx_diff_pairs: list[tuple[int, int]],
        s_current: list[int],
        max_depth: int,
        seen_vals: list[tuple[int, int]] = []
    ):
        global total_sum_diffs
        global switch_diffs

        print('------------------')
        print(f'missing_num: {missing_num}, repeated_vals: {repeated_vals}')
        print('s_current', s_current)
        print('idx_diff_pairs', idx_diff_pairs)
        # print('seen_vals', seen_vals)

        if (total_sum_diffs == 0 or max_depth == 0):
            return switch_diffs
        
        next_switch = get_next_switch(idx_diff_pairs, s_current)
        print('next_switch', next_switch)

        if not next_switch:
            return switch_diffs

        s_new = get_next_s(next_switch, s_current)

        add_item, remove_item = next_switch[1], next_switch[0]
        add_item_idx, add_item_val = add_item[0], add_item[1]
        remove_item_val = remove_item[1]
        seen_vals.append(remove_item)

        new_diffs_by_line_idxs = get_diffs_by_line_idxs(s_new)
        new_total_sum_diffs = get_total_diff(new_diffs_by_line_idxs)
        new_idx_diff_pairs = get_idx_diff_pairs(
            new_diffs_by_line_idxs, s_new, seen_vals)

        # print('new_diffs_by_line_idxs', new_diffs_by_line_idxs)
        print('s_new', s_new)
        # print('new_total_sum_diffs', new_total_sum_diffs)
        # print('new_idx_diff_pairs', new_idx_diff_pairs)

        if new_total_sum_diffs >= total_sum_diffs:
            max_depth -= 1

        total_sum_diffs = new_total_sum_diffs
        switch_diffs += abs(remove_item_val - add_item_val)

        print(
            f'max_depth: {max_depth}, switch_diffs: {switch_diffs}, total_sum_diffs: {total_sum_diffs}')

        if add_item_idx is None:
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

        return update_square(new_idx_diff_pairs, s_new, max_depth, seen_vals)

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

        result = update_square([idx_diff_pair], s_flat, MAX_DEPTH, [])

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
