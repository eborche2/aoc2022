import copy
import math

with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]

monkeys = {}
row = 0
current = None
divisors = []
def process_row_one(row_one):
    number = row_one.split(' ')[1]
    number = number[0: len(number) - 1]
    monkeys[number] = {}
    return number

def process_row_two(row_two, current):
    numbers = row_two.split(':')[1]
    numbers = [int(x) for x in numbers.split(', ')]
    monkeys[current]['numbers'] = numbers

def process_row_three(row_three, current):
    operations = row_three.split('=')[1]
    operations = operations.split(' ')
    del operations[0]
    monkeys[current]['operations'] = operations

def process_row_four(row_four, current):
    divisors.append(int(row_four.split(' ')[3]))
    monkeys[current]['test'] = int(row_four.split(' ')[3])

def process_row_five(row_five, current):
    monkeys[current]['true'] = row_five.split(' ')[5]

def process_row_six(row_six, current):
    monkeys[current]['false'] = row_six.split(' ')[5]

for line in content:
    if 'Monkey' in line:
        row = 0
    if row == 0:
        current = process_row_one(line)
    elif row == 1:
        process_row_two(line, current)
    elif row == 2:
        process_row_three(line, current)
    elif row == 3:
        process_row_four(line, current)
    elif row == 4:
        process_row_five(line, current)
    elif row == 5:
        process_row_six(line, current)
    row += 1

monkeys_base = copy.deepcopy(monkeys)


def run_monkeys(part1, count):
    divisor = math.prod(divisors)
    inspections = [0] * len(monkeys)
    for x in range(count):
        for z in range(len(monkeys)):
            while len(monkeys[str(z)]['numbers']) > 0:
                old = monkeys[str(z)]['numbers'].pop(0)
                if not part1:
                    old %= divisor
                old = eval(' '.join(monkeys[str(z)]['operations']))
                if part1:
                    old = int(old / 3)
                inspections[z] += 1
                if old % monkeys[str(z)]['test'] == 0:
                    monkeys[monkeys[str(z)]['true']]['numbers'].append(old)
                else:
                    monkeys[monkeys[str(z)]['false']]['numbers'].append(old)
    inspections.sort(reverse=True)
    print(inspections[0] * inspections[1])
# Part 1
run_monkeys(True, 20)
monkeys = copy.deepcopy(monkeys_base)
# Part 2
run_monkeys(False, 10000)
