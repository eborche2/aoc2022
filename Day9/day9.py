with open('file.in') as f:
	content = f.readlines()
content = [x.strip().split(' ') for x in content]
head = [0, 0]
tail = [0, 0]
tail_places = set()
tail_places.add((0, 0))
movement = {
    'L': [-1, 0],
    'R': [1, 0],
    'U': [0, 1],
    'D': [0, -1],
}
tail_knots = [[0,0] for x in range(9)]
knot_places = set()
knot_places.add((0,0))


def move_head(direction, current_head):
    current_head[0] += movement[direction][0]
    current_head[1] += movement[direction][1]
    return current_head


def move_tail(current_tail, current_head, iteration=None):
    x_yaw = current_head[0] - current_tail[0]
    y_yaw = current_head[1] - current_tail[1]
    dirc_hor = None
    dirc_vert = None
    if abs(x_yaw) > 1 or abs(y_yaw) > 1:
        if abs(x_yaw) > 0:
            dirc_hor = 'L' if x_yaw < 0 else 'R'
        if abs(y_yaw) > 0:
            dirc_vert = 'D' if y_yaw < 0 else 'U'
    if dirc_hor:
        current_tail[0] += movement[dirc_hor][0]
        current_tail[1] += movement[dirc_hor][1]
    if dirc_vert:
        current_tail[0] += movement[dirc_vert][0]
        current_tail[1] += movement[dirc_vert][1]
    if dirc_hor or dirc_vert:
        if not iteration:
            tail_places.add((current_tail[0], current_tail[1]))
        elif iteration == 8:
            knot_places.add((current_tail[0], current_tail[1]))
    return current_tail


for turn, each in enumerate(content):
    for x in range(int(each[1])):
        head = move_head(each[0], head)
        tail = move_tail(tail, head)
        for i in range(9):
            if i == 0:
                tail_knots[0] = move_tail(tail_knots[0], head, i)
            else:
                tail_knots[i] = move_tail(tail_knots[i], tail_knots[i - 1], i)
        #print(head, each[0], tail_knots)


# Part 1
print(len(tail_places))
# Part 2
print(len(knot_places))