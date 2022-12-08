# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = [[int(h) for h in [*x.strip()]] for x in f.readlines()]


# print(data)


def is_tree_visible(x, y, trees):
    h = trees[y][x]

    l = trees[y][:x]
    v_l = h > max(l)
    r = trees[y][x + 1:]
    v_r = h > max(r)
    t = [trees[i][x] for i in range(0, y)]
    v_t = h > max(t)
    b = [trees[i][x] for i in range(y + 1, len(trees))]
    v_b = h > max(b)
    return v_l or v_r or v_t or v_b


v_in_mid = []
for y, row in enumerate(data):
    if 0 < y < len(data) - 1:
        for x, h in enumerate(row):
            if 0 < x < len(row) - 1:
                if is_tree_visible(x, y, data):
                    v_in_mid.append((x, y))

part1 = len(v_in_mid) + len(data) * 2 + len(data[0]) * 2 - 4
assert part1 == 1789
print("Part 1:", part1)


def get_sc(h, row):
    sc = 0
    for t in row:
        sc += 1
        if t >= h:
            break
    return sc


def get_scenic_score(x, y, trees):
    h = trees[y][x]
    sc_l = get_sc(h, reversed(trees[y][:x]))
    sc_r = get_sc(h, trees[y][x + 1:])
    sc_t = get_sc(h, reversed([trees[i][x] for i in range(0, y)]))
    sc_b = get_sc(h, [trees[i][x] for i in range(y + 1, len(trees))])
    return sc_l * sc_r * sc_t * sc_b


part2 = 0
for y, row in enumerate(data):
    if 0 < y < len(data) - 1:
        for x, h in enumerate(row):
            if 0 < x < len(row) - 1:
                sc_tree = get_scenic_score(x, y, data)
                if sc_tree > part2:
                    part2 = sc_tree
assert part2 == 314820
print("Part 2:", part2)
