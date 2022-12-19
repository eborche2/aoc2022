import copy

with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]

pieces = [
    [(2,0), (3,0), (4,0), (5,0)],
    [(2,1), (3,1), (3,0), (3,2), (4,1)],
    [(4,0), (4,1), (4,2), (3,2), (2,2)],
    [(2,0), (2,1), (2,2), (2,3)],
    [(2,0), (3,0), (2,1), (3,1)]
]
tower = {
    (0,4): '#',
    (1,4): '#',
    (2,4): '#',
    (3,4): '#',
    (4,4): '#',
    (5,4): '#',
    (6,4): '#'
}

drop = {"current_height": 0, "current_diff": 0, "step": 0, "to_add": 0}


def draw_map(map_to_draw):
    xs = []
    ys = []
    for key, value in map_to_draw.items():
        xs.append(key[0])
        ys.append(key[1])
    xs.sort()
    ys.sort()
    for y in range(ys[0], ys[-1] + 1):
        print(y, ' ' if y < 10 else '', end="")
        for x in range(xs[0], xs[-1] + 1):
            spot = (x,y)
            if (x,y) in map_to_draw:
                print(map_to_draw[spot], end="")
            else:
                print('.', end="")
        print("")



def drop_piece(piece, current_tower, wind, wind_spot, fallen, stop, two, drop):
    skip = fallen
    while True:
        if wind_spot < len(wind):
            direction = wind[wind_spot]
            wind_spot += 1
        else:
            _, height = get_depth(current_tower)
            diff = height - drop["current_height"]
            if drop["current_diff"] == diff and two:
                import pdb; pdb.set_trace()
                left = stop - fallen
                jump = fallen - drop["step"]
                times = int(left / jump)
                fallen += times * jump
                skip = fallen
                drop["to_add"] = times * diff
            drop["current_diff"] = diff
            drop["current_height"] = height
            drop["step"] = fallen
            direction = wind[0]
            wind_spot = 1
        strafe = -1 if direction == '<' else 1
        move = []

        for coord in piece:
            new_coord = (coord[0] + strafe, coord[1])
            if 0 > new_coord[0] or new_coord[0] > 6 or new_coord in current_tower:
                move = piece
                break
            else:
                move.append(new_coord)
        move2 = []

        for coord in move:
            new_coord = (coord[0], coord[1] + 1)
            if new_coord in current_tower:
                for coord in move:
                    current_tower[coord] = '#'
                return wind_spot, current_tower, skip
            move2.append(new_coord)
        piece = copy.deepcopy(move2)


def slide_tower(current_depth, current_tower, i):
    next_loc = 0 if (i + 1) == 5 else i + 1
    up_down = [-1, 2, 0, 1, -2]
    new_tower = {}
    new_depth, _ = get_depth(current_tower)

    height = current_depth - new_depth + up_down[next_loc]
    for key, value in current_tower.items():
        new_tower[(key[0], key[1] + height)] = '#'
    return new_tower


def get_depth(current_tower):
    ys = []
    for key, value in current_tower.items():
        ys.append(key[1])
    ys.sort()
    return ys[0], ys[-1]


def count_tower(current_tower):
    ys = []
    for key, value in current_tower.items():
        ys.append(key[1])
    ys.sort()
    return ys[-1] - ys[0]


def build_tower(current_tower, current_pieces, wind, stop, drop, two=False):
    wind_spot = 0
    fallen = 0
    while True:
        for i, piece in enumerate(current_pieces):
            fallen += 1
            depth, _ = get_depth(current_tower)
            wind_spot, current_tower, fallen = drop_piece(piece, current_tower, wind, wind_spot, fallen, stop, two, drop)
            current_tower = slide_tower(depth, current_tower, i)
            if fallen == stop:
                break
        if fallen == stop:
            break
    print(count_tower(current_tower) + drop["to_add"])

# Part One
build_tower(tower, pieces, content[0], 2022)
# We know tower height is steady now. Just use a multiple
# Part Two
build_tower(tower, pieces, content[0], 1000000000000, drop, True)
