# filepath = 'test1.txt'
# filepath = 'test2.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = [x.strip().split() for x in f.readlines()]
    data = [(x[0], int(x[1])) for x in data]


# print(data)


def head_to_right(h, t):
    return h[0] - t[0] == 2


def head_to_left(h, t):
    return t[0] - h[0] == 2


def head_above(h, t):
    return h[1] - t[1] == 2


def head_below(h, t):
    return t[1] - h[1] == 2


def diag_move_3_steps(h, t):
    return abs(h[0] - t[0]) + abs(h[1] - t[1]) == 3


def diag_move_4_steps(h, t):
    return abs(h[0] - t[0]) == abs(h[1] - t[1]) == 2


def print_rope(rope):
    size = 6
    grid = [['.'] * size for _ in range(size - 1)]

    grid[0][0] = 's'
    for i, rope_item in reversed(list(enumerate(rope))):
        char = str(i)
        if i == 0:  # Head
            char = 'H'
        grid[rope_item[1]][rope_item[0]] = char

    print("")
    for row in reversed(grid):
        print("".join(row))


def move_tail(h, t):
    h_x = h[0]
    h_y = h[1]
    t_x = t[0]
    t_y = t[1]

    if diag_move_4_steps(h, t):
        x = t_x + 1 if h_x > t_x else t_x - 1
        y = t_y + 1 if h_y > t_y else t_y - 1
        return x, y

    if diag_move_3_steps(h, t):
        if head_to_right(h, t):
            return t_x + 1, h_y
        elif head_to_left(h, t):
            return t_x - 1, h_y
        elif head_above(h, t):
            return h_x, t_y + 1
        elif head_below(h, t):
            return h_x, t_y - 1

    if head_to_right(h, t):
        return t_x + 1, t_y
    elif head_to_left(h, t):
        return t_x - 1, t_y
    elif head_above(h, t):
        return t_x, t_y + 1
    elif head_below(h, t):
        return t_x, t_y - 1
    return t


def move_part2(rope, dist, delta):
    for step in range(dist):
        for i, _ in enumerate(rope):
            if i == 0:  # Head
                rope[i] = (rope[i][0] + delta[0], rope[i][1] + delta[1])
            else:
                rope[i] = move_tail(rope[i - 1], rope[i])

            if i == len(rope) - 1:
                tail_trail.add(rope[i])
        # print_rope(rope)
    return rope


def move_rope(rope):
    for x in data:
        direction = x[0]
        dist = x[1]
        if direction == 'R':
            rope = move_part2(rope, dist, (1, 0))
        elif direction == 'L':
            rope = move_part2(rope, dist, (-1, 0))
        elif direction == 'U':
            rope = move_part2(rope, dist, (0, 1))
        elif direction == 'D':
            rope = move_part2(rope, dist, (0, -1))


rope = [(0, 0)] * 2
tail_trail = set()
move_rope(rope)

part1 = len(tail_trail)
assert part1 == 6190
print("Part 1:", part1)

rope = [(0, 0)] * 10
tail_trail = set()
move_rope(rope)

part2 = len(tail_trail)
assert part2 == 2516
print("Part 2:", part2)
