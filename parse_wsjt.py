# usage: python parse_wsjt.py

from time import sleep

print('loading db')
from make_short_db import ham_list
print('done')

GRID = 'BP'
COORDS = [2,7,5,8]
STATE = 'AK'

def extract_message_word(line, word_num, column_num_of_message=48):
    message = line[column_num_of_message:]
    words = message.split()
    return words[word_num]

def extract_grid(line):
    return extract_message_word(line, -1)

def extract_call_sign(line):
    # fixme "CQ POTA" breaks word counting
    return extract_message_word(line, 1)

def grid_matches(line, digraph_sought):
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
    results = []
    for entry in ham_list:  # may take forever. fixme with indexing or sort/tree
        if entry[0] == call:
            results += entry[1:]  # just "flat" list of [city,state,zip,city,state,zip,city,...]
    return results

def flag_str(line, loc, grid, coords, state):
    """Make a 3-char string to say whether grid, coords, and state are of
    interest.
    """
    output = ['_']*3
    if len(loc) < 2:  # probably call is non-US and not in DB
        loc_state  = None
    else:
        loc_state = loc[1]  # assumes just 1st state is accurate
    if grid_matches(line, grid):
        output[0] = 'G'
    if coords_match(line, coords[0], coords[1], coords[2], coords[3]):
        output[1] = 'C'
    if loc_state == state:
        output[2] = 'S'
    return ''.join(output)

def looks_like_grid(candidate):
    if len(candidate) != 4:
        return False
    if not candidate[0:2].isalpha():
        return False
    if not candidate[2:].isdigit():
        return False
    return True

def letter2tens(letter):
    for i in range(65, 65 + 26):
        if chr(i) == letter:
            letter_num = i - 65
            tens_place = letter_num *  10
            return tens_place

def grid2xy(grid):
    return [
        letter2tens(grid[0]) + int(grid[2]),
        letter2tens(grid[1]) + int(grid[3])
    ]

def grid2rowcol(grid):
    x_base, y_base = grid2xy('CN78')  # northwest Washington state
    x, y =  grid2xy(grid)
    col_num = x - x_base
    row_num = y_base - y  # note north is high y but low row_num
    return [row_num, col_num]

def grids2map(grids):
    max_row, max_col = grid2rowcol('FL65')
    text_prelim = (('.' * max_col + '\n') * max_row).split()
    text_list = [list(s) for s in text_prelim]  #  list of list, matrix of dots
    for g in grids:
        r, c = grid2rowcol(g)
        try:
            text_list[r][c] = '*'
        except IndexError:
            pass  # assume grid is outside CONUS
    text_block = ''
    for r in text_list:
        line = '  '.join(r)
        text_block += line + '\n'
    return text_block

def tail_once(n_lines, grid, coords, state, style='flags'):
    text_block = ''
    with open('/Users/ajz/Library/Application Support/WSJT-X/ALL.TXT') as fh:
        all_lines = fh.readlines()
        tail = all_lines[(-1 * n_lines):]
        max_len = max([len(s) for s in tail])
        grids = []
        for line in tail:
            call_sign = extract_call_sign(line)
            loc = call2loc(call_sign)
            flags = flag_str(line, loc, grid, coords, state)
            text_block += \
                flags + ' ' + \
                line.rstrip().ljust(max_len + 1) + \
                str(loc) + '\n'

            # map-related stuff
            tentative_grid = extract_grid(line)
            if looks_like_grid(tentative_grid):
                grids.append(tentative_grid)
    text_block += '\n'
    if style == 'flags':
        return text_block
    else:
        return grids2map(grids)

if __name__ == '__main__':
    while True:
        print(tail_once(20, GRID, COORDS, STATE, style='map'))
        sleep(2)
