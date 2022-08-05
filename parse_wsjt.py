# usage is something like:
# watch -n 14 python parse_wsjt.py

def extract_grid(line):
    message = line[48:]  # assume column 48 is start of message
    words = message.split()
    return words[-1]  # assume last word is grid

def grid_matches(line, digraph_sought='DN'):
    grid = extract_grid(line)
    return grid[0:2] == digraph_sought

def coords_match(line, xl, xh, yl, yh):
    grid = extract_grid(line)
    x = int(grid[2])
    y = int(grid[3])
    return (xl <= x <= xh) and (yl <= y <= yh)

def tail_once(n_lines=100):
    with open('/Users/ajz/Library/Application Support/WSJT-X/ALL.TXT') as fh:
        all_lines = fh.readlines()
        tail = all_lines[(-1 * n_lines):]
        for line in tail:
            if grid_matches(line, 'DN'):
                print(line, end='')
                if coords_match(line, 2, 7, 5, 8):  # 2~7 and 5~8 are montana
                    print(' ' * 4, '^' * 60)

tail_once(100)
