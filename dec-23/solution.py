import time

# TEST = True
TEST = False

filepath = "test.txt" if TEST else "input.txt"

with open(filepath, 'r') as f:
    data = [[l for l in line.strip()] for line in f.readlines()]


# print(data)

def draw(elves, round):
    xs = [x for x, y in elves]
    xmin, xmax = min(xs), max(xs)
    width = xmax - xmin + 1
    ys = [y for x, y in elves]
    ymin, ymax = min(ys), max(ys)
    height = ymax - ymin + 1

    elves = [(x - xmin, y - ymin) for x, y in elves]

    grid = [["." for _ in range(width)] for _ in range(height)]

    for x, y in elves:
        grid[y][x] = "#"

    print("")
    print("== End of Round {} ==".format(round))
    print("xmin: {}, xmax: {}, ymin: {}, ymax: {}".format(xmin, xmax, ymin, ymax))
    for row in grid:
        print("".join(row))


def get_elves_positions(grid):
    e = dict()
    for y, line in enumerate(grid):
        for x, _ in enumerate(line):
            if grid[y][x] == "#":
                e[(x, y)] = None
    return e


def get_adjecent_north(x, y):
    return {(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)}


def get_adjecent_south(x, y):
    return {(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)}


def get_adjecent_west(x, y):
    return {(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)}


def get_adjecent_east(x, y):
    return {(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)}


def get_adjecent_all(x, y):
    return get_adjecent_north(x, y) \
        .union(get_adjecent_south(x, y), get_adjecent_west(x, y), get_adjecent_east(x, y))


def get_move_proposals(elves, directions):
    move_propsals = dict()
    for x, y in elves.keys():
        if not get_adjecent_all(x, y).intersection(elves.keys()):
            move_propsals[(x, y)] = x, y
            continue

        for d in directions:
            if d == "N" and not get_adjecent_north(x, y).intersection(elves.keys()):
                move_propsals[(x, y)] = x, y - 1
                break
            elif d == "S" and not get_adjecent_south(x, y).intersection(elves.keys()):
                move_propsals[(x, y)] = x, y + 1
                break
            elif d == "W" and not get_adjecent_west(x, y).intersection(elves.keys()):
                move_propsals[(x, y)] = x - 1, y
                break
            elif d == "E" and not get_adjecent_east(x, y).intersection(elves.keys()):
                move_propsals[(x, y)] = x + 1, y
                break

        if (x, y) not in move_propsals.keys():
            move_propsals[(x, y)] = (x, y)
    return move_propsals


def get_new_positions(move_proposals):
    new_positions = dict()
    for old, new in move_proposals.items():
        if sum(1 for n in move_proposals.values() if n == new) == 1:
            new_positions[new] = None
        else:
            new_positions[old] = None
    return new_positions


def rotate_directions(directions):
    return directions[1:] + [directions[0]]


def get_empty_tiles(elves):
    xs = [x for x, y in elves]
    width = max(xs) - min(xs) + 1
    ys = [y for x, y in elves]
    height = max(ys) - min(ys) + 1

    return width * height - len(elves)


elves = get_elves_positions(data)
print(elves.keys())


def run_part1(elves):
    start = time.time()

    directions = ["N", "S", "W", "E"]
    for i in range(10):
        move_proposals = get_move_proposals(elves, directions)
        elves = get_new_positions(move_proposals)
        directions = rotate_directions(directions)
        draw(elves, i + 1)

    part1 = get_empty_tiles(elves.keys())
    print("Part 1: {}, {:0.2f}s".format(part1, time.time() - start))
    if TEST:
        assert part1 == 110
    else:
        assert part1 == 3877


run_part1(elves)


def run_part2(elves):
    start = time.time()

    directions = ["N", "S", "W", "E"]
    i = 0
    while True:
        move_proposals = get_move_proposals(elves, directions)

        if set(move_proposals.keys()) == set(move_proposals.values()):
            part2 = i + 1
            break

        elves = get_new_positions(move_proposals)
        directions = rotate_directions(directions)
        draw(elves, i + 1)
        i += 1

    print("Part 2: {}, {:0.2f}s".format(part2, time.time() - start))

    if TEST:
        assert part2 == 20
    else:
        assert part2 == 982


elves = get_elves_positions(data)
run_part2(elves)
