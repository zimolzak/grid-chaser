import fileinput

for line in fileinput.input():
    message = line[48:]
    words = message.split()
    grid = words[-1]
    if grid[0:2] == 'DN':
        print(line, end='')
