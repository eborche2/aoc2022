import time

with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]
stone_map = {(500, 0): "+"}
units_of_sand = []

def to_iterate(start, end, side):
    while start[side] != end[side]:
        stone_map[start] = '#'
        if end[side] - start[side] > 0:
            if side == 1:
                start = (start[0], start[1] + 1)
            else:
                start = (start[0] + 1, start[1])
        else:
            if side == 1:
                start = (start[0], start[1] - 1)
            else:
                start = (start[0] - 1, start[1])
        stone_map[start] = '#'


def add_to_map(start, end):
    start = eval('(' + start + ')')
    end = eval('(' + end + ')')
    if start[0] == end[0]:
        to_iterate(start, end, 1)
    else:
        to_iterate(start, end, 0)

for each in content:
    split = each.split(' -> ')
    for x in range(len(split) - 1):
        add_to_map(split[x], split[x + 1])

def print_map():
    xs = []
    ys = []
    for (key, item) in stone_map.items():
        xs.append(key[0])
        ys.append(key[1])
    xs.sort()
    ys.sort()
    for y in range(ys[0], ys[-1] + 1):
        for x in range(xs[0], xs[-1] + 1):
            if (x,y) in stone_map:
                print(stone_map[(x,y)], end="")
            else:
                print(".", end="")
        print("")
    return ys[-1]

def is_infinite(point, max_ys):
    if point[1] == (max_ys + 2):
        return True
    return False

def check_map(start, max_y, part1):
    if part1 and start[1] > max_y:
        return False
    next = (start[0], start[1])
    for adds in [(0, 1), (-1, 0), (2, 0)]:
        next = (next[0] + adds[0], next[1] + adds[1])
        if (not part1 and is_infinite(next, max_y)) or next in stone_map:
            if not is_infinite(next, max_y) and stone_map[next] == '.':
                return next
        else:
            stone_map[next] = '.'
            return next
    stone_map[start] = 'O'
    units_of_sand.append('0')
    if start == (500, 0):
        return False
    return True


def drop_sand(max_yss, partone):
    units_of_sand = []
    while True:
        starts = (500, 0)
        end = False
        while True:
            starts = check_map(starts, max_yss, partone)
            if starts is True:
                break
            if starts is False:
                end = True
                break
        if end:
            break

max_ys = print_map()
drop_sand(max_ys, True)
print_map()
# part 1
print(len(units_of_sand))
start = time.time()
drop_sand(max_ys, False)
print_map()
# Part 2 Not bad 2.8 seconds
print(len(units_of_sand))
end = time.time()
print(end - start)