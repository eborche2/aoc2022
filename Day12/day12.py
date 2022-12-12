with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]

movement = {
    'L': [-1, 0],
    'R': [1, 0],
    'U': [0, 1],
    'D': [0, -1],
}

a_locs = []
def find_S(topography):
    start = None
    end = None
    for y, row in enumerate(topography):
        for x, value in enumerate(row):
            if value == 'S':
                start = (x, y)
            if value == 'E':
                end = (x, y)
            if value == 'a':
                a_locs.append((x, y))
    return start, end

start, end = find_S(content)

def generate_options(spot):
    possibilities = []
    for (key, value) in movement.items():
        test = (spot[0] + value[0], spot[1] + value[1])
        if 0 <= test[0] < len(content[0]) and 0 <= test[1] < len(content):
            possibilities.append(test)
    return possibilities

def walk_tracks(paths):
    finished = []
    shortest = {}
    while len(paths) > 0:
        continuing = []
        for path in paths:
            last = path[-1]
            current = content[last[1]][last[0]]
            options = generate_options(last)
            for potential_coords in options:
                potential = content[potential_coords[1]][potential_coords[0]]
                if potential == 'E' and ord('z') <= ord(current) + 1:
                    new_path = path.copy()
                    new_path.append(potential_coords)
                    finished.append(new_path)
                elif current == 'S' or ord(potential) <= ord(current) + 1 and potential_coords not in path:
                    new_path = path.copy()
                    new_path.append(potential_coords)
                    if potential_coords in shortest and len(new_path) < shortest[potential_coords] or potential_coords not in shortest:
                        shortest[potential_coords] = len(new_path)
                        continuing.append(new_path)
        paths = continuing.copy()
        if len(finished) > 0:
            return len(finished[0]) - 1

def start_multiple_spots():
    lowest = 1000
    for place in a_locs:
        check = walk_tracks([[place]])
        if not check:
            continue
        if check < lowest:
            lowest = check
    return lowest

tracks = [[start]]
# Part 1
print(walk_tracks(tracks))
# part 2
print(start_multiple_spots())
