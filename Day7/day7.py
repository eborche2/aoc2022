with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]


def process_reverse(location):
    paths_dirty = location.split('/')
    paths = []
    for path in paths_dirty:
        if path != '':
            paths.append(path)
    paths.pop()
    if len(paths) == 0:
        return '/'
    return '/' + '/'.join(paths) + '/'


def process_command(command, location, root):
    if command[1] == "cd":
        if command[2] == "..":
            location = process_reverse(location)
        elif command[2] == "/":
            location = "/"
        else:
            location += command[2] + '/'
            root[location] = {}
    return location, root


def process_file_or_folder(entry, location, root):
    if 'total' not in root[location]:
        root[location]['total'] = 0
        root[location]['tally'] = True
    if entry[0] == 'dir':
        root[location][location + entry[1] + '/'] = 0
    else:
        root[location][entry[1]] = int(entry[0])
        root[location]['total'] += int(entry[0])
    if root[location]['total'] > 100000:
        root[location]['tally'] = False
    return root


def clean_up(location, root):
    temp = location
    while temp != '/':
        hold = temp
        temp = process_reverse(hold)
        if not root[hold]['tally']:
            root[temp]['tally'] = False
        else:
            break
    return root


def process_result(root):
    # Too lazy, just forcing it
    changed = True
    while changed:
        changed = False
        for (ukey, uvalue) in root.items():
            for (key, value) in uvalue.items():
                try:
                    if key not in ['total', 'tally'] and '/' in key and value != root[key]['total']:
                        root[ukey]['total'] -= uvalue[key]
                        root[ukey][key] = root[key]['total']
                        root[ukey]['total'] += uvalue[key]
                        if uvalue['total'] > 100000:
                            root[ukey]['tally'] = False
                        changed = True
                except KeyError:
                    changed = True
                    break
    total = 0
    for (key, value) in root.items():
        if root[key]['tally']:
            total += root[key]['total']
    print(total)
    # 1989474
    return root


def find_smallest_to_delete(root):
    left =  70000000 - root['/']['total']
    needed = 30000000 - left
    current = 30000000
    for (key, value) in root.items():
        if root[key]['total'] >= needed:
            if root[key]['total'] < current:
                current = root[key]['total']
    print(current)


def process_list(commands):
    # Too lazy to build a tree
    root = {}
    location = '/'
    root[location] = {}
    switch = False
    for i, entry in enumerate(commands):
        split = entry.split(' ')
        if split[0] == '$':
            if not switch:
                switch = True
                clean_up(location, root)
            location, root = process_command(split, location, root)
        else:
            switch = False
            root = process_file_or_folder(split, location, root)
    # Part 1
    root = process_result(root)
    # Part 2
    find_smallest_to_delete(root)

process_list(content)