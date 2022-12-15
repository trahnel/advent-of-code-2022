import time

# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = [l.strip() for l in f.readlines()]


# print(data)


def get_rocks(data):
    rock_paths = [[[int(y) for y in x.split(",")] for x in r.split(" -> ")] for r in data]

    rocks = set()
    for path in rock_paths:
        for i in range(len(path) - 1):
            p0 = path[i]
            p1 = path[i + 1]
            if p0[0] == p1[0]:  # Enumerate height (Y)
                direction = 1 if p1[1] - p0[1] > 0 else -1
                for y in range(p0[1], p1[1] + direction, direction):
                    rocks.add((p0[0], y))
            else:  # Enumerate X
                direction = 1 if p1[0] - p0[0] > 0 else -1
                for x in range(p0[0], p1[0] + direction, direction):
                    rocks.add((x, p0[1]))
    return rocks


PRINT_CAVE = False


def print_cave(falling_sand, resting_sand, rocks):
    if not PRINT_CAVE:
        return

    depth = max([r[1] for r in rocks])
    left = min([r[0] for r in rocks])
    right = max([r[0] for r in rocks])

    grid = [["." for _ in range(left, right + 1)] for y in range(depth + 1)]
    grid[falling_sand[1]][falling_sand[0] - left] = "+"
    for r in rocks:
        grid[r[1]][r[0] - left] = "#"
    for s in resting_sand:
        grid[s[1]][s[0] - left] = "o"

    y_len = len(str(len(grid) - 1))

    print("")
    for i in range(3):
        print(" " * y_len + " " + str(left)[i] + " " * (500 - left - 1) + str(500)[i] + " " * (right - 500 - 1) +
              str(right)[i])

    for i, y in enumerate(grid):
        print(str(i).rjust(y_len, " "), "".join(y))


def sand_fall(part, falling_sand, resting_sand, rocks, floor=None):
    if part == 1:
        depth = max([r[1] for r in rocks])
        left = min([r[0] for r in rocks])
        right = max([r[0] for r in rocks])
        if falling_sand[0] < left or falling_sand[0] > right or falling_sand[1] > depth:
            return resting_sand, True
    elif part == 2:
        if falling_sand in resting_sand:
            return resting_sand, True

    x = falling_sand[0]
    y = falling_sand[1]

    blocked = resting_sand.union(rocks)
    oob = False
    while falling_sand not in blocked and ((part == 1 and not oob) or (part == 2)):
        if y == floor:
            rocks.add((x, y))
            print_cave(falling_sand, resting_sand, rocks)
        elif (x, y + 1) not in blocked:
            resting_sand, oob = sand_fall(part, (x, y + 1), resting_sand, rocks, floor)
        elif (x - 1, y + 1) not in blocked:
            resting_sand, oob = sand_fall(part, (x - 1, y + 1), resting_sand, rocks, floor)
        elif (x + 1, y + 1) not in blocked:
            resting_sand, oob = sand_fall(part, (x + 1, y + 1), resting_sand, rocks, floor)
        else:
            resting_sand.add((x, y))
            print_cave(falling_sand, resting_sand, rocks)

        blocked = resting_sand.union(rocks)

    return resting_sand, oob


rocks = get_rocks(data)
depth = max([r[1] for r in rocks])
floor = depth + 2
falling_sand = (500, 0)

start_part1 = time.time()
resting_sand = set()
print_cave(falling_sand, resting_sand, rocks)
resting_sand, _ = sand_fall(1, falling_sand, resting_sand, rocks)
part1 = len(resting_sand)
# assert part1 == 24
assert part1 == 1068
print("Part 1: {}, {:0.2f}s".format(part1, time.time() - start_part1))

start_part2 = time.time()
resting_sand = set()
print_cave(falling_sand, resting_sand, rocks)
resting_sand, _ = sand_fall(2, falling_sand, resting_sand, rocks, floor)
part2 = len(resting_sand)
# assert part2 == 93
assert part2 == 27936
print("Part 2: {}, {:0.2f}s".format(part2, time.time() - start_part2))
