with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]
# A 65 a 97
total = 0
total2 = 0
def calc_value(letter):
    if ord(letter) < 97:
        return ord(letter) - 38
    else:
        return ord(letter) - 96
for sack in content:
    for x in range(int(len(sack)/2)):
        if sack[x] in sack[int(len(sack)/2):]:
            total += calc_value(sack[x])
            break
# Part 1
print(total)
for x, sack in enumerate(content):
    if x == 0 or x % 3 == 0:
        for item in sack:
            if item in content[x + 1] and item in content[x + 2]:
                total2 += calc_value(item)
                break
# Part 2
print(total2)
