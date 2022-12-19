import time

# TEST = True
TEST = False

filepath = "test.txt" if TEST else "input.txt"

with open(filepath, 'r') as f:
    cubes = set([tuple([int(coord) for coord in line.strip().split(",")]) for line in f.readlines()])

print(cubes)


def get_adjacent(cube):
    x, y, z = cube
    left = (x - 1, y, z)
    right = (x + 1, y, z)
    above = (x, y + 1, z)
    under = (x, y - 1, z)
    behind = (x, y, z + 1)
    front = (x, y, z - 1)
    return {left, right, above, under, behind, front}


def run_part1():
    start = time.time()

    part1 = 0
    for c in cubes:
        adj = get_adjacent(c)
        exposed = 6 - len(cubes.intersection(adj))
        part1 += exposed

    print("Part 1: {}, {:0.2f}s".format(part1, time.time() - start))


run_part1()

xs = [x for x, y, z in cubes]
ys = [y for x, y, z in cubes]
zs = [z for x, y, z in cubes]
minx, maxx, miny, maxy, minz, maxz = min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)


def can_exit(cube, seen):
    if cube in seen:
        return False

    x, y, z = cube
    seen.add(cube)

    if x < minx or x > maxx or y < miny or y > maxy or z < minz or z > maxz:
        return True
    elif cube in cubes:
        return False
    else:
        adj = get_adjacent(cube)
        for a in adj:
            exit = can_exit(a, seen)
            if exit:
                return True

    return False


def run_part2():
    start = time.time()

    part2 = 0
    for c in cubes:
        adj = get_adjacent(c)

        for a in adj:
            if can_exit(a, set()):
                part2 += 1
            # else:
            #     print(a)

    print("Part 2: {}, {:0.2f}s".format(part2, time.time() - start))


run_part2()
