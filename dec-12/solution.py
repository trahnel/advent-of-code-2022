# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = [[*x.strip()] for x in f.readlines()]

for d in data:
    print("".join(d))


def print_steps(visited, grid):
    board = [[val for val in r] for r in grid]
    for coord, distance in visited.items():
        x = coord[0]
        y = coord[1]
        board[y][x] += str(distance)

    board = [[val.rjust(5, " ") for val in r] for r in board]
    print("")
    print("  " + "".join([str(i).rjust(5, " ") for i in range(len(grid[0]))]))
    for i, row in enumerate(board):
        print("{}{}".format(str(i).rjust(2, " "), "".join(row)))


def get_adjecent_coords(pos, w, h):
    x = pos[0]
    y = pos[1]
    return [a for a in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if 0 <= a[0] < w and 0 <= a[1] < h]


def get_steps_part1(positions, grid, visited):
    h = len(grid)
    w = len(grid[0])
    steps = {}
    for coord, distance in positions.items():
        x = coord[0]
        y = coord[1]
        val = grid[y][x]
        pos_ord = ord('a') if val == 'S' else ord(val)

        adj_coords = [c for c in get_adjecent_coords(coord, w, h) if c not in visited.keys()]
        adj_step_heights = [(pos_adj, ord(grid[pos_adj[1]][pos_adj[0]]) - pos_ord) for pos_adj in adj_coords]

        [steps.update({s[0]: distance + 1}) for s in adj_step_heights if
         s[1] <= 1 and grid[s[0][1]][s[0][0]].islower() or val == 'y' and grid[s[0][1]][
             s[0][0]] == 'E']  # y is before z which is the height of E

    visited.update(positions)
    print_steps(visited, grid)

    if [s for s in steps.items() if grid[s[0][1]][s[0][0]] == 'E']:
        # Reached the peak
        visited.update(steps)
        print_steps(visited, grid)
        return visited

    return get_steps_part1(steps, grid, visited)


def get_position(c, grid):
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == c:
                return x, y


steps = {get_position("S", data): 0}
steps = get_steps_part1(steps, data, {})
part1 = max(steps.values())
assert part1 == 425
print("Part 1:", part1)


def get_steps_part_2(positions, grid, visited):
    h = len(grid)
    w = len(grid[0])
    steps = {}
    for coord, distance in positions.items():
        x = coord[0]
        y = coord[1]
        val = grid[y][x]
        pos_ord = ord('z') if val == 'E' else ord(val)

        adj_coords = [c for c in get_adjecent_coords(coord, w, h) if c not in visited.keys()]
        adj_step_heights = [(pos_adj, pos_ord - ord(grid[pos_adj[1]][pos_adj[0]])) for pos_adj in adj_coords]

        [steps.update({s[0]: distance + 1}) for s in adj_step_heights if
         s[1] <= 1 and grid[s[0][1]][s[0][0]].islower()]

    visited.update(positions)
    print_steps(visited, grid)

    if [s for s in steps.items() if grid[s[0][1]][s[0][0]] == 'a']:
        visited.update(steps)
        print_steps(visited, grid)
        return visited

    return get_steps_part_2(steps, grid, visited)


steps = {get_position("E", data): 0}
steps = get_steps_part_2(steps, data, {})
part2 = max(steps.values())
assert part2 == 418
print("Part 2:", part2)
