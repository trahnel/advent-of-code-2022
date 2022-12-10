# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = [x.strip().split() for x in f.readlines()]
# print(data)

x_pos = 1
X = [1]
for cmd in data:
    if cmd[0] == "noop":
        X.append(X[len(X) - 1])
    elif cmd[0] == "addx":
        X.extend([X[len(X) - 1], X[len(X) - 1] + int(cmd[1])])


def get_signal_strength(i, x):
    return x[i - 1] * i


part1 = sum([get_signal_strength(s, X) for s in range(20, len(X), 40)])
assert part1 == 12520
print("Part 1:", part1)


def get_sprite(x):
    return list(range(x - 1, x + 2))


sprite = get_sprite(x_pos)
screen = []
for i, x in enumerate(X):
    sprite = get_sprite(x)
    screen.append("#") if i % 40 in sprite else screen.append(".")

print("")
print("Part 2:")
[print("".join(screen[x:x + 40])) for x in range(0, len(screen) - 1, 40)]
