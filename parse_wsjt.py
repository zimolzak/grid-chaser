# usage is something like:
# watch -n 14 python parse_wsjt.py

print('loading db')
from make_short_db import ham_list
print('done')

def extract_message_word(line, word_num, column_num_of_message=48):
    message = line[column_num_of_message:]
    words = message.split()
    return words[word_num]

def extract_grid(line):
    return extract_message_word(line, -1)

def extract_call_sign(line):
    return extract_message_word(line, 1)

def grid_matches(line, digraph_sought='DN'):
    if digraph_sought == 'any' or digraph_sought == 'all':
        return True
    grid = extract_grid(line)
    return grid[0:2] == digraph_sought

def coords_match(line, xl, xh, yl, yh):
    grid = extract_grid(line)
    if len(grid) < 4:
        # Really it's last word of msg. Might be '73' not grid.
        return False
    try:
        x = int(grid[2])
        y = int(grid[3])
    except ValueError:  # assume it tried to cast letter or "/" to int.
        return False
    return (xl <= x <= xh) and (yl <= y <= yh)

def call2loc(call):
    results = ''
    for entry in ham_list:  # may take forever. fixme with indexing or sort/tree
        if entry[0] == call:
            one_result = ' '.join(entry[1:])
            results += one_result + '. '
    return results

def flag_str(line, loc, grid='EM', coords=[2,7,5,8], state='MT'):
    """make a 3-char string to say whether grid, coords, state are of interest."""
    output = "   "
    loc_state = loc.split()[1]
    if grid_matches(line, grid):
        output[0] = 'G'
    if coords_match(line, coords[0], coords[1], coords[2], coords[3]):
        output[1] = 'C'
    if loc_state == state:
        output[2] = 'S'
    return output

def tail_once(n_lines=100):
    with open('/Users/ajz/Library/Application Support/WSJT-X/ALL.TXT') as fh:
        all_lines = fh.readlines()
        tail = all_lines[(-1 * n_lines):]
        max_len = max([len(s) for s in tail])
        for line in tail:
            if grid_matches(line, 'EM'):
                call_sign = extract_call_sign(line)
                loc = call2loc(call_sign)
                print(line.rstrip().ljust(max_len + 1), loc)
                if coords_match(line, 2, 7, 5, 8):  # 2~7 and 5~8 are montana
                    print(' ' * 4, '^' * 60)

tail_once(n_lines=20)
