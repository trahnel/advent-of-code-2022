import functools

# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = f.read()
# print(data)

pairs = [[eval(val) for val in pairs.split()] for pairs in data.split("\n\n")]


def compare(l, r):
    if isinstance(l, int) and isinstance(r, int):
        if l < r:
            return -1
        elif l > r:
            return 1
        else:
            return 0

    if isinstance(l, list) and isinstance(r, list):
        for i in range(max(len(l), len(r))):
            try:
                l1 = l[i]
            except IndexError:
                return -1
            try:
                r1 = r[i]
            except IndexError:
                return 1
            result = compare(l1, r1)
            if result == 0:
                continue
            else:
                return result
        return 0
    elif isinstance(l, int) and isinstance(r, list):
        return compare([l], r)
    elif isinstance(l, list) and isinstance(r, int):
        return compare(l, [r])


part1 = 0
for i, pair in enumerate(pairs, 1):
    left, right = pair
    order = compare(left, right)

    if order == -1:
        part1 += i
assert part1 == 6240
print("Part 1:", part1)

packets = [eval(packet) for packet in data.split()]
packets.extend([[[2]], [[6]]])

sorted_packets = sorted(packets, key=functools.cmp_to_key(compare))
part2 = (sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1)
assert part2 == 23142
print("Part 2:", part2)
