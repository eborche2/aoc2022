import copy

ship = {
    "1": ["N", "S", "D", "C", "V", "Q", "T"],
    "2": ["M", "F", "V"],
    "3": ["F", "Q", "W", "D", "P", "N", "H", "M"],
    "4": ["D", "Q", "R", "T", "F"],
    "5": ["R", "F", "M", "N", "Q", "H", "V", "B"],
    "6": ["C", "F", "G", "N", "P", "W", "Q"],
    "7": ["W", "F", "R", "L", "C", "T"],
    "8": ["T", "Z", "N", "S"],
    "9": ["M", "S", "D", "J", "R", "Q", "H", "N"]
}
ship2 = copy.deepcopy(ship)
with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]

for each in content:
    row = each.split(' ')
    total = int(row[1])
    crane9001 = []
    for x in range(total):
        try:
            popped = ship[row[3]].pop()
            popped2 = ship2[row[3]].pop()
            crane9001.append(popped2)
            ship[row[5]].append(popped)
        except IndexError:
            pass
    crane9001.reverse()
    ship2[row[5]] += crane9001
for (key, value) in ship.items():
    # Part 1
    print(value[-1], end = '')
print(" ")
for (key, value) in ship2.items():
    # Part 2
    print(value[-1], end = '')
print(" ")