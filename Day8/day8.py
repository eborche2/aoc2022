with open('file.in') as f:
	content = f.readlines()
matrix = [[ int(z) for z in x.strip()] for x in content]

found = set()
width = len(matrix[0]) - 1
height = len(matrix) - 1
view_meter = {}
max_scene = 0

def calc_scene(coords, max_scene):
    # Was trying to avoid this and had to do it for part 2 anyway :(
    location_value = matrix[coords[1]][coords[0]]
    scenes = [0, 0, 0, 0]
    for i, direction in enumerate([(1, 0), (-1, 0), (0, 1), (0, -1)]):
        stop = False
        moving = [coords[0], coords[1]]
        while not stop:
            moving[0] += direction[0]
            moving[1] += direction[1]
            if moving[0] < 0 or moving[1] < 0:
                stop = True
                continue
            try:
                if matrix[moving[1]][moving[0]] >= location_value:
                    stop = True
                scenes[i] += 1
            except IndexError:
                stop = True
    view_meter[coords] = scenes[0] * scenes[1] * scenes[2] * scenes[3]
    if view_meter[coords] > max_scene:
        max_scene = view_meter[coords]
    return max_scene

for y in range(height + 1):
    records = [None, None, None, None]
    for x in range(width + 1):
        left = (x, y)
        top = (y, x)
        right = (width - x, height - y)
        bot = (height - y, width - x)
        for spot, each in enumerate([left, top, right, bot]):
            if each[0] == 0 or each[1] == 0 or each[0] == width or each[1] == height:
                found.add(each)
            value = matrix[each[1]][each[0]]
            if records[spot] is None or value > records[spot]:
                records[spot] = value
                found.add(each)
            if each not in view_meter:
                max_scene = calc_scene(each, max_scene)
# Part 1
print(len(found))
# Part 2
print(max_scene)