import time

# TEST = True
TEST = False

filepath = "test.txt" if TEST else "input.txt"

with open(filepath, 'r') as f:
    jet = [j for j in f.read()]

# print(jet)

rocks = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (1, 0), (0, 1), (1, 1))
]


def draw(falling, landed):
    h_grid = 0
    if falling:
        h_grid = max(h_grid, max([y for x, y in falling]) + 1)
    if landed:
        h_grid = max(max([y for x, y in landed]) + 1, h_grid)

    grid = [["." for _ in range(7)] for _ in range(h_grid)]

    if falling:
        for x, y in falling:
            grid[y][x] = "@"

    for x, y in landed:
        grid[y][x] = "#"
    grid.reverse()

    print("")
    for g in grid:
        print("|" + "".join(g) + "|")
    print("".join(["+", "-", "-", "-", "-", "-", "-", "-", "+"]))


next_rock = 0


def new_rock(landed_rocks):
    global next_rock
    h = max(y for x, y in landed_rocks) + 1 if landed_rocks else 0
    rock = {(x + 2, y + h + 3) for x, y in rocks[next_rock]}
    next_rock = 0 if next_rock == len(rocks) - 1 else next_rock + 1
    return rock


ground = {(x, -1) for x in range(7)}


def rock_fall(falling, landed, fall_count):
    if not falling:
        falling = new_rock(landed)
    else:
        falling_temp = {(x, y - 1) for x, y in falling}
        if falling_temp.intersection(ground) or falling_temp.intersection(landed):
            landed.update(falling)
            falling = None
            fall_count += 1
        else:
            falling = falling_temp

    return falling, landed, fall_count


next_jet = 0


def jet_push(falling, landed):
    global next_jet
    jet_direction = -1 if jet[next_jet] == "<" else 1
    next_jet = 0 if next_jet == len(jet) - 1 else next_jet + 1
    if next_jet == 0:
        pass

    falling_moved = {(x + jet_direction, y) for x, y in falling}
    falling_moved_xs = [x for x, y in falling_moved]
    if min(falling_moved_xs) < 0 or max(falling_moved_xs) > 6 or falling_moved.intersection(landed):
        return falling
    else:
        return falling_moved


def run_part1():
    start = time.time()

    falling = None
    landed = set()
    fall_count = 0
    while True:
        falling, landed, fall_count = rock_fall(falling, landed, fall_count)
        # draw(falling, landed)

        if falling:
            falling = jet_push(falling, landed)
            # draw(falling, landed)

        if fall_count == 2022 and not falling:
            part1 = max(y for x, y in landed) + 1
            draw(falling, landed)
            break
    print("Part 1: {}, {:0.2f}s".format(part1, time.time() - start))


run_part1()


def get_height(coords):
    return max([y for x, y in coords]) + 1


next_rock = 0
next_jet = 0


def run_part2():
    start = time.time()

    falling = None
    landed = set()
    prev_landed = set()
    rocks_cycles = []
    fall_count = 0

    h_after_landed = []
    while True:
        falling, landed, fall_count = rock_fall(falling, landed, fall_count)

        if falling:
            falling = jet_push(falling, landed)

        # A rock has landed
        if not falling:
            h_after_landed.append(get_height(landed))

            # All rocks have fallen one round
            if next_rock == 0:
                current_rock_cycle = landed.difference(prev_landed)
                prev_landed = landed.copy()
                current_rock_cycle_h_dy = sum(get_height(r) for r in rocks_cycles)
                current_rock_cycle = {(x, y - current_rock_cycle_h_dy) for x, y in current_rock_cycle}
                current_rock_cycle = sorted(current_rock_cycle)

                if current_rock_cycle in rocks_cycles:
                    cycle_end_index = len(rocks_cycles)
                    cycle_start_index = rocks_cycles.index(current_rock_cycle)

                    # Make sure two rock cycles are matching
                    if rocks_cycles[-1] == rocks_cycles[cycle_start_index - 1]:
                        cycle_length = cycle_end_index - cycle_start_index

                        start_rock_count = cycle_start_index * 5
                        start_height = sum(get_height(r) for r in rocks_cycles[:cycle_start_index])
                        cycle_height = sum(get_height(r) for r in rocks_cycles[cycle_start_index:cycle_end_index])

                        cycle_height_zero = h_after_landed[cycle_start_index * 5 - 1]
                        cycle_rock_heights = [y - cycle_height_zero for y in h_after_landed[cycle_start_index * 5:-5]]
                        break

                rocks_cycles.append(sorted(current_rock_cycle))

    tower = 1000000000000

    rocks_after_start = tower - start_rock_count

    cycle_rock_count = cycle_length * 5
    number_of_cycles = rocks_after_start // cycle_rock_count
    cycles_height = number_of_cycles * cycle_height
    rocks_after_cycles = rocks_after_start - number_of_cycles * cycle_rock_count
    height_after_cycles = 0 if rocks_after_cycles == 0 else cycle_rock_heights[rocks_after_cycles - 1]
    part2 = start_height + cycles_height + height_after_cycles
    print("Part 2: {}, {:0.2f}s".format(part2, time.time() - start))
    if TEST:
        assert part2 == 1514285714288
    else:
        assert part2 == 1580758017509


run_part2()
