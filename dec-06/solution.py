# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = f.read()

print(data)


def get_start_of_message(data, markers):
    return [len(set(data[i:i + markers])) for i in range(0, len(data)) if i < len(data) - markers + 1].index(
        markers) + markers


markers = 4
part1 = get_start_of_message(data, markers)
assert part1 == 1287
print(part1)

markers = 14
part2 = part1 = get_start_of_message(data, markers)
assert part2 == 3716
print(part2)
