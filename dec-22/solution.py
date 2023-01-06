import re
import time

# TEST = True
TEST = False

filepath = "test.txt" if TEST else "input.txt"

with open(filepath, 'r') as f:
    map_grid, path = f.read().split("\n\n")

print(map_grid)
print(path)


def get_map(grid):
    map = dict()
    for y, row in enumerate(grid.split("\n")):
        for x, v in enumerate(row):
            if v in [".", "#"]:
                map[x, y] = v
    return map


map = get_map(map_grid)

moves = re.split('([^0-9])', path)
print(moves)

directions = ["R", "D", "L", "U"]

max_x = max(x for x, y in map.keys())
max_y = max(y for x, y in map.keys())


def get_edges_part1():
    e = dict()
    for y in range(max_y + 1):
        minx = min(x for x, yy in map.keys() if yy == y)
        maxx = max(x for x, yy in map.keys() if yy == y)
        e[maxx + 1, y, "R"] = minx, y, "R"
        e[minx - 1, y, "L"] = maxx, y, "L"

    for x in range(max_x + 1):
        miny = min(y for xx, y in map.keys() if xx == x)
        maxy = max(y for xx, y in map.keys() if xx == x)
        e[x, maxy + 1, "D"] = x, miny, "D"
        e[x, miny - 1, "U"] = x, maxy, "U"

    return e


edges = get_edges_part1()


def draw(pos, map):
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for c, v in map.items():
        x, y = c
        grid[y][x] = v

    posx, posy = pos
    grid[posy][posx] = "X"

    print("")
    for row in grid:
        print("".join(row))


def follow_path(start, moves, map, edges):
    direction = "R"

    pos = start
    for m, move in enumerate(moves):
        if move.isnumeric():
            for i in range(int(move)):
                next = None
                pos_x, pos_y = pos
                if direction == "R":
                    next = pos_x + 1, pos_y
                elif direction == "L":
                    next = pos_x - 1, pos_y
                elif direction == "D":
                    next = pos_x, pos_y + 1
                elif direction == "U":
                    next = pos_x, pos_y - 1

                n = *next, direction
                if n in edges.keys():
                    next = edges[n][0:2]

                    if map[next] == "#":
                        break
                    direction = edges[n][2]

                if map[next] == "#":
                    break

                pos = next
            print("Direction={} Move={} Progress={}/{}".format(direction, move, m + 1, len(moves)))
            # draw(pos, map)

        elif move == "R":
            dir_index = (directions.index(direction) + 1) % len(directions)
            direction = directions[dir_index]
        elif move == "L":
            dir_index = (directions.index(direction) - 1) % len(directions)
            direction = directions[dir_index]
    return pos, direction


def run_part1(edges):
    start = time.time()

    entrance = min(x for x, y in map if y == 0), 0
    pos, direction = follow_path(entrance, moves, map, edges)

    print("Final position", pos, direction)

    pos_x, pos_y = pos
    part1 = 1000 * (pos_y + 1) + 4 * (pos_x + 1) + directions.index(direction)
    print("Part 1: {}, {:0.2f}s".format(part1, time.time() - start))
    if TEST:
        assert part1 == 6032
    else:
        assert part1 == 109094


# run_part1(edges)


def get_edges_part2():
    if TEST:
        section_len = 4
    else:
        section_len = 50

    e = dict()
    if TEST:
        for i in range(section_len):
            e[12, i, "R"] = 15, 11 - i, "L"  # A
            e[16, 11 - i, "R"] = 11, i, "L"  # A

            e[12, 4 + i, "R"] = 15 - i, 8, "D"  # B
            e[15 - i, 7, "U"] = 11, 4 + i, "L"  # B

            e[8, i, "L"] = 4 + i, 4, "D"  # C
            e[4 + i, 3, "U"] = 8, i, "R"  # C

            e[8 + i, -1, "U"] = 3 - i, 4, "D"  # D
            e[3 - i, 3, "U"] = 8 + i, 0, "D"  # D

            e[-1, 4 + i, "L"] = 15 - i, 11, "U"  # E
            e[15 - i, 12, "D"] = i, 4 + i, "R"  # E

            e[i, 8, "D"] = 11 - i, 11, "U"  # F
            e[11 - i, 12, "D"] = i, 7, "U"  # F

            e[7, 8 + i, "L"] = 7 - i, 7, "U"  # G
            e[8, 7 - i, "D"] = 8, 8 + i, "R"  # G
    else:
        for i in range(section_len):
            e[50 + i, -1, "U"] = 0, 150 + i, "R"  # A
            e[-1, 150 + i, "L"] = 50 + i, 0, "D"  # A

            e[100 + i, -1, "U"] = i, 199, "U"  # B
            e[i, 200, "D"] = 100 + i, 0, "D"  # B

            e[149, i, "R"] = 99, 149 - i, "L"  # C
            e[100, 149 - i, "R"] = 149, i, "L"  # C

            e[100 + i, 50, "D"] = 99, 50 + i, "L"  # D
            e[100, 50 + i, "R"] = 100 + i, 49, "U"  # D

            e[50 + i, 150, "D"] = 49, 150 + i, "L"  # E
            e[50, 150 + i, "R"] = 50 + i, 149, "U"  # E

            e[49, i, "L"] = 0, 149 - i, "R"  # F
            e[-1, 149 - i, "L"] = 50, i, "R"  # F

            e[49, 50 + i, "L"] = i, 100, "D"  # G
            e[i, 99, "U"] = 50, 50 + i, "R"  # G

    return e


edges = get_edges_part2()


def run_part2(edges):
    start = time.time()

    entrance = min(x for x, y in map if y == 0), 0
    pos, direction = follow_path(entrance, moves, map, edges)

    print("Final position", pos, direction)

    pos_x, pos_y = pos
    part2 = 1000 * (pos_y + 1) + 4 * (pos_x + 1) + directions.index(direction)
    print("Part 2: {}, {:0.2f}s".format(part2, time.time() - start))
    if TEST:
        assert part2 == 5031
    else:
        assert part2 == 53324


run_part2(edges)
