with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]

def split_convert(row):
    entries = row.split(',')
    entry1 = entries[0].split('-')
    entry2 = entries[1].split('-')
    return [int(entry1[0]), int(entry1[1]), int(entry2[0]), int(entry2[1])]

def check_contains(row):
    check = False
    if row[2] <= row[0] <= row[3] and row[2] <= row[1] <= row[3]:
        check = True
    elif row[0] <= row[2] <= row[1] and row[0] <= row[3] <= row[1]:
        check = True
    return check

def check_overlap(row):
    check = False
    if row[2] <= row[0] <= row[3] or row[2] <= row[1] <= row[3]:
        check = True
    elif row[0] <= row[2] <= row[1] or row[0] <= row[3] <= row[1]:
        check = True
    return check

totals = 0
totals2 = 0
for each in content:
    if check_contains(split_convert(each)):
        totals += 1
    if check_overlap(split_convert(each)):
        totals2 += 1
# Part 1
print(totals)
# Part 2
print(totals2)