# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = f.readlines()

data = [line.strip() for line in data]

print(data)


def get_ids(id_span):
    first, last = map(int, id_span.split('-'))
    return set([i for i in range(first, last + 1)])


part1 = 0
for pair in data:
    e1, e2 = pair.split(',')
    x1 = get_ids(e1)
    x2 = get_ids(e2)
    if x1.issubset(x2) or x1.issuperset(x2):
        part1 += 1

print('Part1:', part1)

part2 = 0
for pair in data:
    e1, e2 = pair.split(',')
    x1 = get_ids(e1)
    x2 = get_ids(e2)
    if not x1.isdisjoint(x2):
        part2 += 1

print('Part2:', part2)
