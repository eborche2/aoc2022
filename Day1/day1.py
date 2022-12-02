
with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]
totals = []
last = 0
for n in content:
    if n == '':
        totals.append(last)
        last = 0
    else:
        last += int(n)
totals.sort()
# First
print(totals[-1])
# Second
print(totals[-1] + totals[-2] + totals[-3])