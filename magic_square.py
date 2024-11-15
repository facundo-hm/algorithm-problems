# Problem in progress

def forming_magic_square(s: list[list[int]]):
    MAGIC_NUM = 15

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
        s_current: list[int]
    ):
        diff_by_idxs = get_diffs_by_square_idx(diffs_by_line_idxs)
        print('diff_by_idxs', diff_by_idxs)
        
        idx_average_diffs = [
            s_current[idx_diffs]
            + round(sum(line_diffs) / len(line_diffs))
            for idx_diffs, line_diffs in enumerate(diff_by_idxs)]

        idx_diff_pairs = [
            pair
            for pair in zip(range(len(s_current)), idx_average_diffs)
            if s_current[pair[0]] != pair[1]]

        return sorted(
            idx_diff_pairs,
            key=lambda pair: abs(s_current[pair[0]] - pair[1]))
    
    def get_total_diff(line_diffs: list[int]):
        return sum([abs(diff) for diff in line_diffs])

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
        repeated_vals = set()

        for idx, val in enumerate(s_flat):
            rest = s_flat[idx+1:]

            if val in rest:
                repeated_vals.add(val)

        return repeated_vals

    def get_next_switch(
        idx_diff_pairs: list[tuple[int, int]], s_current:list[int]
    ):
        first_item = idx_diff_pairs[0]
        first_item_diff: int = first_item[1]
        remove_item = (first_item[0], s_current[first_item[0]])

        if first_item_diff in missing_num:
            return (remove_item, (None, first_item_diff))
        
        if first_item_diff in s_current:
            return (
                remove_item,
                (s_current.index(first_item_diff), first_item_diff))

    initial_diffs_by_line_idxs = get_diffs_by_line_idxs(s_flat)
    print('initial_diffs_by_line_idxs', initial_diffs_by_line_idxs)

    initial_idx_diff_pairs = get_idx_diff_pairs(
        initial_diffs_by_line_idxs, s_flat)
    initial_idx_diff_pairs = [(1, 9), (2, 3), (8, 7), (6, 8), (7, 3)]
    print('initial_idx_diff_pairs', initial_idx_diff_pairs)
    
    total_sum_diffs = get_total_diff(initial_diffs_by_line_idxs)
    print('initial_total_diff', total_sum_diffs)

    missing_num = get_missing_numbers(s_sorted)
    print('missing_num', missing_num)
    
    repeated_vals = get_repeated_vals()
    print('repeated_vals', repeated_vals)

    def update_square(
        idx_diff_pairs: list[tuple[int, int]], s_current: list[int]
    ):
        print('///////////////////////////////')

        print('missing_num', missing_num)
        print('repeated_vals', repeated_vals)

        print('idx_diff_pairs', idx_diff_pairs)
        print('s_current', s_current)

        global total_sum_diffs
        global switch_diffs

        if not len(idx_diff_pairs) or total_sum_diffs == 0:
            return switch_diffs

        next_switch = get_next_switch(idx_diff_pairs, s_current)
        print('next_switch', next_switch)

        if not next_switch:
            next_idx_diff_pairs = idx_diff_pairs[1:]
            return update_square(next_idx_diff_pairs, s_current)

        add_item, remove_item = next_switch[1], next_switch[0]
        add_item_idx, add_item_val = add_item[0], add_item[1]
        remove_item_idx, remove_item_val = (
            remove_item[0], remove_item[1])
        s_new = s_current[:]
        s_new[remove_item_idx] = add_item_val

        if add_item_idx is not None:
            s_new[add_item_idx] = remove_item_val

        print('s_new', s_new)

        new_diffs_by_line_idxs = get_diffs_by_line_idxs(s_new)
        print('new_diffs_by_line_idxs', new_diffs_by_line_idxs)

        new_idx_diff_pairs = get_idx_diff_pairs(
            new_diffs_by_line_idxs, s_new)
        print('new_idx_diff_pairs', new_idx_diff_pairs)
        
        new_total_sum_diffs = get_total_diff(new_diffs_by_line_idxs)
        print('new_total_sum_diffs', new_total_sum_diffs)

        if new_total_sum_diffs <= total_sum_diffs:
            total_sum_diffs = new_total_sum_diffs
            switch_diffs += abs(remove_item_val - add_item_val)

            if add_item_idx is None:
                missing_num.remove(add_item_val)

                if remove_item_val not in repeated_vals:
                    missing_num.append(remove_item_val)
                else:
                    repeated_vals.remove(remove_item_val)

            return update_square(new_idx_diff_pairs, s_new)
        
        next_idx_diff_pairs = idx_diff_pairs[1:]
        return update_square(next_idx_diff_pairs, s_current)

    return update_square(initial_idx_diff_pairs, s_flat)

test_case_0 = [[4, 9, 2], [3, 5, 7], [8, 1, 5]]
test_case_0_result = 1

test_case_1 = [[4, 8, 2], [4, 5, 7], [6, 1, 6]]
test_case_1_result = 4

test_case_2 = [[4, 5, 8], [2, 4, 1], [1, 9, 7]]
test_case_2_result = 14

test_case_18 = [[6, 9, 8], [3, 9, 4], [9, 4, 4]]
test_case_18_result = 21

result = forming_magic_square(test_case_1)
print('result', result)
