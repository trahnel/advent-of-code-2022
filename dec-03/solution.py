# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = f.readlines()

data = [line.strip() for line in data]


# print(data)

def get_priority(c):
    if c.isupper():
        return ord(c) - 38
    else:
        return ord(c) - 96


part1 = 0
for rucksack in data:
    half = int(len(rucksack) / 2)
    c1 = set(rucksack[:half])
    c2 = set(rucksack[half:])

    c = c1.intersection(c2)
    part1 += get_priority(c.pop())

assert part1 == 7737
print('Part1:', part1)

part2 = 0
for i in range(0, len(data), 3):
    c1 = set(data[i])
    c2 = set(data[i + 1])
    c3 = set(data[i + 2])
    c = c1.intersection(c2).intersection(c3)
    part2 += get_priority(c.pop())

assert part1 == 2697
print('Part2:', part2)
