import time

# TEST = True
TEST = False

filepath = "test.txt" if TEST else "input.txt"

with open(filepath, 'r') as f:
    data = [line.strip() for line in f.readlines()]

# print(data)

walls = set()
blizzards = set()
entrance = 1, 0
expeditions = {entrance}
exit = None

for y, row in enumerate(data):
    for x, val in enumerate(row):
        if val == "#":
            walls.add((x, y))
        elif val in [">", "<", "^", "v"]:
            blizzards.add((x, y, val))

        if y == len(data) - 1 and val == ".":
            exit = x, y

maxx = max([x for x, y in walls])
maxy = max([y for x, y in walls])


def get_adjecent(x, y):
    return set(a for a in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if 0 <= a[0] < maxx and 0 <= a[1] < maxy + 1)


def draw(expeditions, blizzards, walls):
    grid = [["." for _ in range(maxx + 1)] for _ in range(maxy + 1)]

    for x, y, v in blizzards:
        grid[y][x] = v
    for x, y in walls:
        grid[y][x] = "#"
    for x, y in expeditions:
        grid[y][x] = "E"

    for row in grid:
        print("".join(row))


def move_blizzards(blizzards, walls):
    moved_blizzards = set()
    for b in blizzards:
        x, y, v = b
        if v == ">":
            moved = (x + 1, y, v)
            if moved[0:2] not in walls:
                moved_blizzards.add(moved)
            else:
                moved_blizzards.add((1, y, v))
        elif v == "<":
            moved = (x - 1, y, v)
            if moved[0:2] not in walls:
                moved_blizzards.add(moved)
            else:
                moved_blizzards.add((maxx - 1, y, v))
        elif v == "v":
            moved = (x, y + 1, v)
            if moved[0:2] not in walls:
                moved_blizzards.add(moved)
            else:
                moved_blizzards.add((x, 1, v))
        elif v == "^":
            moved = (x, y - 1, v)
            if moved[0:2] not in walls:
                moved_blizzards.add(moved)
            else:
                moved_blizzards.add((x, maxy - 1, v))
    return moved_blizzards


def move_expedition(expedition, blizzards, walls):
    ex, ey = expedition
    adj = get_adjecent(ex, ey)
    adj.add(expedition)  # We can wait in the same spot
    bs_poss = set((x, y) for x, y, v in blizzards)
    paths = adj.difference(walls).difference(bs_poss)
    return paths


def minute(expeditions, blizzards, walls):
    blizzards = move_blizzards(blizzards, walls)
    exps = set()
    for pos in expeditions:
        new_poss = move_expedition(pos, blizzards, walls)
        for n in new_poss:
            exps.add(n)
    return exps, blizzards


def run_part1(expeditions, blizzards, walls):
    start = time.time()

    part1 = 0
    while exit not in expeditions:
        print("\nMinute", part1 + 1)
        expeditions, blizzards = minute(expeditions, blizzards, walls)
        # print("Expeditions", expeditions)
        # draw(expeditions, blizzards, walls)
        part1 += 1

    print("Part 1: {}, {:0.2f}s".format(part1, time.time() - start))
    if TEST:
        assert part1 == 18
    else:
        assert part1 == 322


run_part1(expeditions, blizzards, walls)


def run_part2(expeditions, blizzards, walls):
    start = time.time()

    targets = [exit, entrance, exit]
    target = targets.pop()
    part2 = 0
    while True:
        print("\nMinute", part2 + 1)
        expeditions, blizzards = minute(expeditions, blizzards, walls)
        # draw(expeditions, blizzards, walls)
        part2 += 1

        if target in expeditions:
            expeditions = {target}

            if not targets:
                # print("\nFinal:")
                # draw(expeditions, blizzards, walls)
                break

            target = targets.pop()
            draw(expeditions, blizzards, walls)

    print("Part 2: {}, {:0.2f}s".format(part2, time.time() - start))
    if TEST:
        assert part2 == 54
    else:
        assert part2 == 974


run_part2(expeditions, blizzards, walls)
