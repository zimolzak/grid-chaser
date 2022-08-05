# import fileinput

# for line in fileinput.input():
#     message = line[48:]
#     words = message.split()
#     grid = words[-1]
#     if grid[0:2] == 'DN':
#         print(line, end='')

def tail_once():
    with open('/Users/ajz/Library/Application Support/WSJT-X/ALL.TXT') as fh:
        all_lines = fh.readlines()
        tail = all_lines[-25:]
        for line in tail:
            print(line, end='')

tail_once()
