# usage is something like:
# watch -n 14 python parse_wsjt.py

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

def tail_once(n_lines=100):
    with open('/Users/ajz/Library/Application Support/WSJT-X/ALL.TXT') as fh:
        all_lines = fh.readlines()
        tail = all_lines[(-1 * n_lines):]
        for line in tail:
            if grid_matches(line, 'all'):
                print(extract_call_sign(line), line, end='')
                if coords_match(line, 2, 7, 5, 8):  # 2~7 and 5~8 are montana
                    print(' ' * 4, '^' * 60)

tail_once(n_lines=20)
