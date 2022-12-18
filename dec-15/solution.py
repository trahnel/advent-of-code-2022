import re
import time

# TEST = True
TEST = False

if TEST:
    filepath = 'test.txt'
    target_y = 10
    boundry = 20
else:
    filepath = 'input.txt'
    target_y = 2000000
    boundry = 4000000

with open(filepath, 'r') as f:
    data = [[int(numbers) for numbers in re.findall(r"-?\d+", line)] for line in f.readlines()]

coords = {tuple(d[:2]): tuple(d[2:]) for d in data}


# print(coords)


def draw(coords, nba):
    left = min([min(s[0], b[0]) for s, b in coords.items()])
    left = min(left, min([nb[0] for nb in no_beacon_area]))
    right = max([max(s[0], b[0]) for s, b in coords.items()])
    right = max(right, max([nb[0] for nb in no_beacon_area]))
    top = min([min(s[1], b[1]) for s, b in coords.items()])
    top = min(top, min([nb[1] for nb in no_beacon_area]))
    bottom = max([max(s[1], b[1]) for s, b in coords.items()])
    bottom = max(bottom, max([nb[1] for nb in no_beacon_area]))

    grid = [["." for _ in range(left, right + 1)] for y in range(top, bottom + 1)]

    for nb in nba:
        grid[nb[1] - top][nb[0] - left] = "#"

    for s, b in coords.items():
        print(s)
        grid[s[1] - top][s[0] - left] = "S"
        grid[b[1] - top][b[0] - left] = "B"

    y_len = len(str(len(grid) - 1))

    print("")
    h1 = "".join([str(x).rjust(2, " ")[0] for x in range(left, right + 1)])
    h2 = "".join([str(x).rjust(2, " ")[1] for x in range(left, right + 1)])

    print("  ", h1)
    print("  ", h2)

    for i, y in enumerate(grid, top):
        print(str(i).rjust(y_len, " "), "".join(y))


def get_no_beacon_area(pair, target_y, existing, part):
    s, b = pair
    dist = abs(s[0] - b[0]) + abs(s[1] - b[1])

    area = set()
    # # Above beacon
    l = 0
    for y in range(s[1] - dist, s[1]):
        if (part == 1 and y == target_y) or (part == 2 and 0 <= y <= target_y) or TEST:
            for x in range(-l, l + 1):
                if part == 1 or (part == 2 and 0 <= x <= target_y):
                    c = s[0] + x, y
                    if c not in existing:
                        # print('ABOVE', x, y)
                        area.add(c)
        l += 1

    # Same y as beacons
    y = s[1]
    if (part == 1 and y == target_y) or (part == 2 and 0 <= y <= target_y) or TEST:
        for x in range(-dist, dist + 1):
            if part == 1 or (part == 2 and 0 <= x <= target_y):
                c = s[0] + x, s[1]
                if c not in existing:
                    # print('SAME', x, y)
                    area.add(c)

    # Below beacon
    l = 0
    for y in range(s[1] + dist, s[1], -1):
        if (part == 1 and y == target_y) or (part == 2 and 0 <= y <= target_y) or TEST:
            for x in range(-l, l + 1):
                if part == 1 or (part == 2 and 0 <= x <= target_y):
                    c = s[0] + x, y
                    if c not in existing:
                        # print('BELOW', x, y)
                        area.add(c)
        l += 1
    return area


existing = set(coords.keys()).union(set(coords.values()))

# PART 1
# start = time.time()
# no_beacon_area = set()
# for item in coords.items():
#     no_beacons = get_no_beacon_area(item, target_y, existing, 1)
#     no_beacon_area.update(no_beacons)
#
# if TEST:
#     draw(coords, no_beacon_area)
#     part1 = len([nb for nb in no_beacon_area if nb[1] == target_y])
# else:
#     part1 = len(no_beacon_area)
# print("Part 1: {}, {} sec".format(part1, time.time() - start))
# if TEST:
#     assert part1 == 26
# else:
#     assert part1 == 5125700

# PART 2
start = time.time()
# no_beacon_area = set((x, y) for x in range(boundry + 1) for y in range(boundry + 1))
no_beacon_area = set()
for item in coords.items():
    no_beacons = get_no_beacon_area(item, boundry, existing, 2)
    no_beacon_area.update(no_beacons)

if TEST:
    draw(coords, no_beacon_area)

full_area = set((x, y) for x in range(boundry + 1) for y in range(boundry + 1))
part2 = full_area.difference(no_beacon_area).difference(existing)

print("Part 2: {}, {} sec".format(part2, time.time() - start))

if TEST:
    assert part2 == {(14, 11)}
# else:
#     assert part2 == 5125700
