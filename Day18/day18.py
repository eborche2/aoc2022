import copy

with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]

locations = [eval('(' + x + ')') for x in content]

permutations = [
    [(-1,-1,-1), (-1,0,-1), (-1,-1,0), (-1,0,0)],
    [(-1,-1,-1), (-1,0,-1), (0,-1,-1), (0,0,-1)],
    [(-1,-1,-1), (0,-1,0), (0,-1,-1),(-1,-1,0)],
    [(0,0,0), (-1,0,-1), (0,0,-1), (-1,0,0)],
    [(0,0,0), (-1,0,0), (-1,-1,0), (0,-1,0)],
    [(0,0,0), (0,0,-1), (0,-1,-1), (0,-1,0)]
]
def get_sides(point):
    sides = []
    for each in permutations:
        new_side = []
        for side in each:
            new_side.append((point[0] + side[0], point[1] + side[1], point[2] + side[2]))
        new_side.sort()
        sides.append(new_side)
    return sides


def get_point(sides, side):
    # Find the side and get the square it would be facing.
    adjust = [(-1, 0, 0), (0, 0, -1), (0, -1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0)]
    for i, match in enumerate(sides):
        if match == side:
            new_sides = []
            for new_side in sides:
                n_side = []
                for point in new_side:
                    n_side.append((point[0] + adjust[i][0], point[1] + adjust[i][1], point[2] + adjust[i][2]))
                n_side.sort()
                new_sides.append(n_side)
            return new_sides


def find_cube(side, all_sides):
    for each in all_sides:
        if side in each:
            return get_point(each, side)


def eliminate_sides(sides, all_sides):
    # check each potential cube. If all the sides of the possible cube are in the sides list, it is air tight.
    keep_sides = []
    for side in sides:
        new_cube = find_cube(side, all_sides)
        for new_side in new_cube:
            if new_side not in sides:
                keep_sides.append(side)
                break
    return keep_sides


def calculate_position(positions):
    total_sides = []
    all_sides = []
    for position in positions:
        sides = get_sides(position)
        all_sides.append(sides)
        for side in sides:
            if side in total_sides:
                total_sides.remove(side)
            else:
                total_sides.append(side)
    # Part 1
    print(len(total_sides))
    # Part 2 2546
    print(len(eliminate_sides(total_sides, all_sides)))


calculate_position(locations)
