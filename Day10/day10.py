with open('file.in') as f:
	content = f.readlines()
content = [x.strip().split(' ') for x in content]

cycle_checks = [20, 60, 100, 140, 180, 220]
values = []
reg = 1
cycle = 0
regs = [1]
for x, value in enumerate(content):

    if len(value) == 1:
        cycle += 1
        regs.append(reg)
        if cycle in cycle_checks:
            values.append(reg)
    else:
        for z in range(2):
            cycle += 1
            regs.append(reg)
            if cycle in cycle_checks:
                values.append(reg)
    if len(value) > 1:
        reg += int(value[1])

result = 0
for i, each in enumerate(cycle_checks):
    result += each * values[i]
# Part 1
print(result)
# Part 2
add = 0
for z in range(1, 7):
    for x in range(40):
        check = x + add + 1
        sprite = regs[check]
        draw = '.'
        if x == sprite or x == sprite - 1 or x == sprite + 1:
            draw = '#'
        if (x + 1) % 40 == 0:
            print(draw)
        else:
            print(draw, end = "")
    add += 40