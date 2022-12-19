import time
import copy

with open('file.in') as f:
	content = f.readlines()
content = [x.strip() for x in content]

def create_valve_map(lines):
    valves = {}
    ignore = []
    for line in lines:
        parts = line.split(';')
        check = parts[0].split(' ')
        key = check[1]
        valves[key] = {'flow' : int(check[4].split('=')[1]), 'valves': []}
        if valves[key]['flow'] == 0:
            ignore.append(key)
        check = parts[1].split(' valves ')
        if len(check) == 1:
            check = parts[1].split(' valve ')
            valves[key]['valves'].append(check[1])
            continue
        check = check[1].split(', ')
        for each in check:
            valves[key]['valves'].append(each)
    return valves, ignore

valve_map, ignore_valves = create_valve_map(content)


def find_shortest(start, key, valves):
    paths = [{'paths': [start], 'length': 0}]
    shortest = None
    path = []
    while len(paths) > 0:
        new_paths = []
        for path in paths:
            if key in valves[path['paths'][-1]]['valves']:
                path['length'] += 1
                if not shortest or (shortest and path['length']):
                    shortest = path['length']
                    path = copy.deepcopy(path)
                    path['paths'].append(key)
                    break
            for new_valve in valves[path['paths'][-1]]['valves']:
                new_path = copy.deepcopy(path)
                new_path['paths'].append(new_valve)
                new_path['length'] += 1
                if len(new_path['paths']) == len(set(new_path['paths'])):
                    new_paths.append(new_path)
        paths = copy.deepcopy(new_paths)
    return shortest, path


def distance_calculator(valves):
    distances = {}
    paths = {}
    for key1, value1 in valves.items():
        start = key1
        for key, value in valves.items():
            if key != start:
                shortest, path = find_shortest(start, key, valves)
                distances[(start, key)] = shortest
                paths[(start, key)] = path
    return distances, paths


valve_distances, valve_paths = distance_calculator(valve_map)


def find_paths(path, valves, ignore):
    key = path['path'][-1]
    paths = []
    release_valve = False
    if key not in ignore and key not in path['open']:
        release_valve = True
    path['total'] += path['flow']
    if release_valve:
        release_path = copy.deepcopy(path)
        release_path['open'].append(key)
        release_path['flow'] += valves[key]['flow']
        paths.append(release_path)
    for valve in valves[key]['valves']:
        some_path = copy.deepcopy(path)
        some_path['path'].append(valve)
        paths.append(some_path)
    return paths


def process_flows(path, ignore, flows, left, local, distances, distances_paths, valves):
    paths = []
    start = path['path'][-1]
    for key, item in flows.items():
        if start == key:
            continue
        length = distances[(start, key)]
        for each in distances_paths[(start, key)]['paths']:
            if each not in path['open'] and each not in ignore and each not in path and start != each:
                local += valves[each]['flow'] * (left - distances[(start, each)])
        paths += distances_paths[(start, key)]['paths']
        left -= length
        local += valves[key]['flow'] * left
        start = paths[-1]
    return local


def reduce_paths(paths, tic, valves, ignore, distances, distance_paths):
    count = []
    reduced = []
    for i, path in enumerate(paths):
        local = path['total'] + (path['flow'] * (30 - tic))
        current = path['path'][-1]
        left = 30 - tic
        flows = {}
        for key, item in valves.items():
            if key not in ignore and key not in path['open'] and current != key:
                flows[key] = item['flow']
        flows = {k: v for k, v in sorted(flows.items(), key=lambda item: item[1], reverse=True)}
        count.append(process_flows(path, ignore, flows, left, local, distances, distance_paths, valves))
    max_value = max(count)
    print(count)
    for i, c in enumerate(count):
        if len(count) < 10000 and c + 500 >= max_value:
            reduced.append(paths[i])
        elif len(count) > 10000 and c + 100 >= max_value:
            reduced.append(paths[i])
    return reduced


def part1(valves, ignore, distances, distance_paths):
    start = [{'total': 0, 'flow': 0, 'open': [], 'path': ['AA']}]
    for tic in range(30):
        next_paths = []
        for path in start:
            next_paths += find_paths(path, valves, ignore)
        start = copy.deepcopy(next_paths)
        start = reduce_paths(start, tic, valves, ignore, distances, distance_paths)
        print(tic, len(start))
    totals = []
    for item in start:
        totals.append(item['total'])
    print(max(totals))

# Part1
part1(valve_map, ignore_valves, valve_distances, valve_paths)

