import time
import copy

with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]

cave_map = {}
points = []
giant_corners = []
def split_points(coords):
    for each in coords:
        split1 = each.split(':')
        group = []
        for value in range(2):
            sections = split1[value].split(',')
            x = int(sections[0].split('=')[1])
            y = int(sections[1].split('=')[1])
            group.append((x, y))
        cave_map[group[0]] = 'S'
        cave_map[group[1]] = 'B'
        points.append(copy.deepcopy(group))


def calculate_distance(s, b):
    valuex = s[0] - b[0]
    valuey = s[1] - b[1]
    return abs(valuex) + abs(valuey)


split_points(content)
def draw_map():
    spiral_map = copy.deepcopy(cave_map)
    for pair in points:
        distance = calculate_distance(pair[0], pair[1])
        spiral_map = spiral_out(distance, pair[0], spiral_map)

    xs = []
    ys = []
    for key, value in spiral_map.items():
        xs.append(key[0])
        ys.append(key[1])
    xs.sort()
    ys.sort()
    for y in range(ys[0], ys[-1] + 1):
        print(y, end="")
        for x in range(xs[0], xs[-1] + 1):
            spot = (x,y)
            if (x,y) in spiral_map:
                print(spiral_map[spot], end="")
            else:
                print('.', end="")
        print("")


def check_row(y, local_map):
    # Worked with spiral out
    xs = []
    ys = []
    for key, value in local_map.items():
        xs.append(key[0])
        ys.append(key[1])
    xs.sort()
    ys.sort()
    count = 0
    for x in range(xs[0], xs[-1] + 1):
        coords = (x, y)
        if coords in local_map:
            if local_map[coords] == '#':
                count += 1
    return count


def spiral_out(max_distance, sensor, spiral_map):
    # This worked but took too long
    sensor_assignment = [sensor[0], sensor[1]]
    start = [copy.deepcopy(sensor_assignment), copy.deepcopy(sensor_assignment), copy.deepcopy(sensor_assignment), copy.deepcopy(sensor_assignment)]
    dirs = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    stops = [False, False, False, False]
    current = copy.deepcopy(start)
    while False in stops:
        for i, each in enumerate(start):
            check = calculate_distance(sensor, each)
            if check >= max_distance:
                stops[i] = True
        for i, dir in enumerate(dirs):
            current[i][0] += dir[0]
            current[i][1] += dir[1]
        for i, point in enumerate(current):
            check = calculate_distance(sensor, point)
            if check > max_distance:
                slide = i + 1
                if slide == 4:
                    slide = 0
                start[i][0] += dirs[slide][0]
                current[i][0] = start[i][0]
                start[i][1] += dirs[slide][1]
                current[i][1] = start[i][1]
                continue
            coords = (current[i][0], current[i][1])
            if coords in spiral_map:
                if spiral_map[coords] == '.':
                    spiral_map[coords] = '#'
            else:
                spiral_map[coords] = '#'
    return spiral_map

def check_line(spot, sensor):
    if spot[0] == sensor[0]:
        if spot[1] > sensor[1]:
            return ['N', spot]
        else:
            return ['S', spot]
    elif spot[1] == sensor[1]:
        if spot[0] > sensor[0]:
            return ['E', spot]
        else:
            return ['W', spot]
    return False



def get_corners(check, sensor):
    corners = {}
    corners[check[0]] = check[1]
    if check[1][0] == sensor[0]:
        distance = abs(check[1][1] - sensor[1])
    else:
        distance = abs(check[1][0] - sensor[0])
    map_dirs = {
        'E': (1,0),
        'W': (-1, 0),
        'N': (0, 1),
        'S': (0, -1)
    }
    for key, value in map_dirs.items():
        if key not in corners:
            corners[key] = (sensor[0] + (distance * value[0]), sensor[1] + (distance * value[1]))
    return corners


def line_check(pivot, behind, ahead, row):
    points = []
    for each in [behind, ahead]:
        slope = int((each[0] - pivot[0]) / (each[1] - pivot[1]))
        intercept = int(pivot[1] - (slope * pivot[0]))
        points.append((int((row - intercept) / slope), row))
    return points


def find_intersections(row, corners):
    if corners['S'][1] <= row <= corners['N'][1]:
        if corners['S'][1] == row:
            return [corners['S']]
        elif corners['N'][1] == row:
            return [corners['N']]
        elif row == corners['E'][1]:
            return [corners['W'], corners['E']]
        elif row > corners['E'][1]:
            return line_check(corners['N'], corners['W'], corners['E'], row)
        elif row < corners['E'][1]:
            return line_check(corners['S'], corners['W'], corners['E'], row)
    return None


def perimeter_draw(max_distance, spot, sensor, row):
    check = check_line(spot, sensor)
    if check is False:
        up = None
        down = None
        dirs = [[1, 1], [-1, -1], [1, -1], [-1, 1]]
        for dir in dirs:
            next_spot= (spot[0] + dir[0], spot[1] + dir[1])
            distance = calculate_distance(sensor, next_spot)
            if distance == max_distance:
                if dir[1] == 1:
                    up = [next_spot, dir]
                else:
                    down = [next_spot, dir]
        scan = [up, down]
        while check is False:
            for i, pair in enumerate(scan):
                check = check_line(pair[0], sensor)
                if check is False:
                    next_spot = (pair[0][0] + pair[1][0], pair[0][1] + pair[1][1])
                    scan[i] = [next_spot, pair[1]]
                else:
                    break
    corners = get_corners(check, sensor)
    giant_corners.append(corners)
    return find_intersections(row, corners)


def pull_perimeter_points(y, perimeter, local_map):
    start= None
    end = None
    for each in perimeter:
        if each[1] == y:
            if not start:
                start = each
            else:
                end = each
    if start:
        if start not in local_map:
            local_map[start] = '#'
        while end and start != end:
            start = (start[0] + 1, start[1])
            if start not in local_map:
                local_map[start] = '#'
    return local_map


def part1(row):
    part1_map = copy.deepcopy(cave_map)
    for pair in points:
        distance = calculate_distance(pair[0], pair[1])
        check = perimeter_draw(distance, pair[1], pair[0], row)
        if check:
            part1_map = pull_perimeter_points(row, check, part1_map)
    print(check_row(row, part1_map))

def review_points(points, part2_map, row):
    doubles = []
    singles = []
    for each in points:
        if len(each) == 1:
            singles.append(each)
        else:
            doubles.append((each[0][0], each[1][0]))
    shuffling = True
    while shuffling:
        shuffling = False
        new_round = []
        while len(doubles) > 0:
            shake = False
            current = doubles.pop()
            if len(new_round) == 0:
                new_round.append(current)
                continue
            for i, latest in enumerate(new_round):
                new_start = None
                new_end = None
                if current[0] < latest[0] and current[1] >= latest[0]:
                    new_start = current[0]
                    shuffling = shake = True
                if current[1] > latest[1] and current[0] <= latest[1]:
                    new_end = current[1]
                    shuffling = shake = True
                if current[0] > latest[0] and current[1] < latest[1]:
                    shuffling = shake = True
                    break
                if shake:
                    new_round[i] = (new_start if new_start is not None else latest[0], new_end if new_end is not None else latest[1])
            if not shake:
                new_round.append(current)
        doubles = copy.deepcopy(new_round)
    doubles.sort()
    x = 0
    for values in doubles:
        if values[0] < x:
            x = values[1]
            continue
        else:
            x += 1
            while x < values[0]:
                if (x, row) not in singles and (x, row) not in cave_map:
                    print(x*4000000 + row)
                    return True
                x += 1
    return False

def part2(end):
    for y in range(end + 1):
        points = []
        for each in giant_corners:
            result = find_intersections(y, each)
            if result:
                points.append(result)
        stop = review_points(points, cave_map, y)
        if stop:
            break


#part1 14 seconds
start = time.time()
part1(2000000)
end = time.time()
print("Part 1 Time", end - start)
#part2 143 seconds could be optimized, but I can't look at it anymore :)
start = time.time()
part2(4000000)
end = time.time()
print("Part 2 Time", end - start)