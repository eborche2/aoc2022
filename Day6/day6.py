with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]

def check_letters(letters):
    set_letters = set(letters)
    if len(set_letters) == len(letters):
        return True
    return False
check = []
def run_letters(count):
    for x, value in enumerate(content[0]):
        if len(check) == count:
            del check[0]
        check.append(value)
        if len(check) == count:
            if check_letters(check):
                print(x + 1)
                break

# Part 1
run_letters(4)
# Part 2
run_letters(14)
