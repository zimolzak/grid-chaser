# import fileinput

def grid_matches(line):
    message = line[48:]
    words = message.split()
    grid = words[-1]
    return grid[0:2] == 'DN'

def tail_once():
    with open('/Users/ajz/Library/Application Support/WSJT-X/ALL.TXT') as fh:
        all_lines = fh.readlines()
        tail = all_lines[-100:]
        for line in tail:
            if grid_matches(line):
                print(line, end='')

tail_once()
