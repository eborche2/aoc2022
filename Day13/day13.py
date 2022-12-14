import math
import time
import copy
with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]
process = content.copy()
count = []

# for x in range(0, len(content), 3):
#     check = len(count)
#     left_string = [t for t in process[x]]
#     right_string = [t for t in process[x + 1]]
#     import pdb; pdb.set_trace()
#     while True:
#         if len(left_string) > 0:
#             left = left_string.pop(0)
#         if len(right_string) > 0:
#             right = right_string.pop(0)
#         else:
#             count.append((x/3) + 1)
#             break
#         if left == right:
#             continue
#         elif not left.isdigit() and not right.isdigit():
#             if left == ']' or right == ']':
#                 if left == ']' and right.isdigit():
#                     count.append((x/3) + 1)
#                     break
#                 elif right == ']' and left.isdigit():
#                     break
#                 if left == ']' and len(left_string) == 1:
#                     count.append((x/3) + 1)
#                     break
#                 elif left == ']':
#                     while len(left_string) > 0 and left in [',', ']']:
#                         left = left_string.pop(0)
#                 elif right == ']':
#                     while len(right_string) > 0 and right in [',', ']']:
#                         right = right_string.pop(0)
#                 if left == right:
#                     continue
#                 elif left == ']':
#                     count.append((x/3) + 1)
#                 break
#             else:
#                 import pdb; pdb.set_trace()
#         while len(left_string) > 0 and left != ']' and (left.isdigit() or right.isdigit()):
#             if right.isdigit() and not left.isdigit():
#                 left = left_string.pop(0)
#             elif left.isdigit() and left_string[0].isdigit():
#                 left += left_string.pop(0)
#             else:
#                 break
#         while len(right_string) > 0 and right != ']' and (right.isdigit() or left.isdigit()):
#             if left.isdigit() and not right.isdigit():
#                 right = right_string.pop(0)
#             elif right.isdigit() and right_string[0].isdigit():
#                 right += right_string.pop(0)
#             else:
#                 break
#         if left.isdigit() and not right.isdigit():
#             break
#         elif not left.isdigit() and right.isdigit():
#             count.append((x/3) + 1)
#             break
#         elif left.isdigit() and right.isdigit():
#             if int(left) < int(right):
#                 count.append((x/3) + 1)
#                 break
#             elif int(left) > int(right):
#                 break
#             continue
#         else:
#             import pdb; pdb.set_trace()
#             print(left, right)
#     if len(count) == check:
#         print(process[x], "<- divider ->", process[x + 1])
#         print(' ')
#         #import pdb; pdb.set_trace()

def process_next(left, right):
    reset = False
    if not isinstance(left, list):
        left = [left]
        reset = True
    if not isinstance(right, list):
        right = [right]
        reset = True
    if reset:
        return process_next(left, right)
    #import pdb; pdb.set_trace()
    next_left = None
    next_right = None
    left_end = False
    right_end = False
    if isinstance(left, list):
        if len(left) > 0:
            next_left = left.pop(0)
        else:
            left_end = True
    if isinstance(right, list):
        if len(right) > 0:
            next_right = right.pop(0)
        else:
            right_end = True
    if left_end and not right_end:
        return True
    elif right_end and not left_end:
        return False
    elif left_end and right_end:
        return None
    if not isinstance(next_left,list) and not isinstance(next_right, list):
        if next_left < next_right:
            return True
        if next_right < next_left:
            return False
        if next_right == next_left:
            return process_next(left, right)
    next_row = process_next(next_left, next_right)
    if next_row is True or next_row is False:
        return next_row
    return process_next(left, right)


for x in range(0, len(content), 3):
    check = len(count)
    left_string = eval(process[x])
    right_string = eval(process[x + 1])
    check = None
    while check is None and check is not False:
        check = process_next(left_string, right_string)
        if len(left_string) == 0 and len(right_string) == 0:
            break
    if check is True:
        count.append((x/3) + 1)
# Part1
print(int(math.fsum(count)))


master_list = []
for x in range(0, len(content), 3):
    master_list.append(eval(process[x]))
    master_list.append(eval(process[x + 1]))
master_list.append([[2]])
master_list.append([[6]])
start = time.time()
shuffled = True
location_two = 0
location_6 = 0
while shuffled:
    shuffled = False
    for x in range(0, len(master_list) - 1):
        left_string = copy.deepcopy(master_list[x])
        if left_string == [[2]]:
            location_two = x + 1
        if left_string == [[6]]:
            location_six = x + 1
        right_string = copy.deepcopy(master_list[x + 1].copy())
        check = None
        while check is None and check is not False:
            check = process_next(left_string, right_string)
            if len(left_string) == 0 and len(right_string) == 0:
                break
        if check is False:
            shuffled = True
            temp = copy.deepcopy(master_list[x])
            master_list[x] = copy.deepcopy(master_list[x + 1])
            master_list[x + 1] = temp
            break
end = time.time()
print(end - start)
# Part 2 Not performative, took 121 seconds.
print(location_two * location_six)