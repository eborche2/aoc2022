
with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]

rps_map = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C'
}
lose_map = {
    'A': 'C',
    'B': 'A',
    'C': 'B'
}
win_map = {
    'A': 'B',
    'B': 'C',
    'C': 'A'
}
total = 0
total2 = 0
for switch in [False, True]:
    total2 = total
    total = 0
    for pair in content:
        choice = rps_map[pair[2]]
        if switch:
            if pair[2] == 'X':
                choice = lose_map[pair[0]]
            elif pair[2] == 'Y':
                choice = pair[0]
            else:
                choice = win_map[pair[0]]

        if choice == 'A':
            total += 1
        elif choice == 'B':
            total += 2
        else:
            total += 3
        if pair[0] == choice:
            total += 3
        elif pair[0] == 'C' and choice == 'A':
            total += 6
        elif pair[0] == 'A' and choice == 'B':
            total += 6
        elif pair[0] == 'B' and choice == 'C':
            total += 6

# Part 1
print(total2)
# Part 2
print(total)