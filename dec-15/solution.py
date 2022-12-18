import re
import time

# TEST = True
TEST = False

if TEST:
    filepath = 'test.txt'
    y_target = 10
    boundry = 20
else:
    filepath = 'input.txt'
    y_target = 2000000
    boundry = 4000000

with open(filepath, 'r') as f:
    data = [[int(numbers) for numbers in re.findall(r"-?\d+", line)] for line in f.readlines()]

coords = {tuple(d[:2]): tuple(d[2:]) for d in data}


def within_boundries(coord, max):
    if 0 <= coord[0] < max and 0 <= coord[1] <= max:
        return True
    return False


def get_border(part, pair, y_target):
    print(pair)
    s, b = pair

    dist = abs(s[0] - b[0]) + abs(s[1] - b[1])

    border = {}
    outer = set()
    for d in range(dist + 1):
        y_above = s[1] - d
        y_below = s[1] + d
        dx = dist - d
        x_left = s[0] - dx
        x_right = s[0] + dx

        if (part == 1 and y_above == y_target) or part == 2:
            border[y_above] = [x_left, x_right]
        if (part == 1 and y_below == y_target) or part == 2:
            border[y_below] = [x_left, x_right]

        if part == 2:
            o = (x_left - 1, y_above)
            if within_boundries(o, y_target):
                outer.add(o)
            o = (x_right + 1, y_above)
            if within_boundries(o, y_target):
                outer.add(o)
            o = (x_left - 1, y_below)
            if within_boundries(o, y_target):
                outer.add(o)
            o = (x_right + 1, y_below)
            if within_boundries(o, y_target):
                outer.add(o)

    if part == 2:
        outer.add((s[0], s[1] - dist - 1))  # Add diamond top
        outer.add((s[0], s[1] + dist + 1))  # Add diamond bottom
    return border, outer


def is_within(coord, sensor_bound):
    cx, cy = coord
    if cy in sensor_bound.keys() and sensor_bound.get(cy)[0] <= cx <= sensor_bound.get(cy)[1]:
        return True
    else:
        return False


def run_part1():
    start = time.time()
    borders = []
    for c in coords.items():
        b, o = get_border(1, c, y_target)
        borders.append(b)

    all_y_vals = set()
    for y in borders:
        if y:
            y_borders = y.get(y_target)
            y_vals = set(range(y_borders[0], y_borders[1] + 1))
            all_y_vals.update(y_vals)
    y_target_sensors = set(x[0] for x in coords.keys() if x[1] == y_target)
    y_target_beacons = set(x[0] for x in coords.values() if x[1] == y_target)

    part1 = len(all_y_vals.difference(y_target_sensors).difference(y_target_beacons))
    print("Part 1: {}, {:0.2f}s".format(part1, time.time() - start))


run_part1()


def run_part2():
    start = time.time()
    borders = []
    outers = set()
    for c in coords.items():
        b, o = get_border(2, c, boundry)
        borders.append(b)
        outers.update(o)

    outside_coord = None
    for o in outers:
        outside = True
        for b in borders:
            if is_within(o, b):
                outside = False
                break

        if outside:
            outside_coord = o
            break

    part2 = outside_coord[0] * 4000000 + outside_coord[1]
    print("Part 2: {}, {:0.2f}s".format(part2, time.time() - start))


run_part2()
