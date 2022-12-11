import math

# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = [[r.strip() for r in x.strip().split("\n")] for x in f.read().split("\n\n")]


class Monkey:
    def __init__(self, data):
        self.items = [int(i) for i in data[1].split(': ')[1].split(', ')]
        self.operation = data[2].split('= ')[1]
        self.divisible_by = int(data[3].split('by ')[1])
        self.true_monkey = int(data[4].split('monkey ')[1])
        self.false_monkey = int(data[5].split('monkey ')[1])
        self.inspections = 0

    def __repr__(self):
        return repr(
            "items={}, operation={}, divisible_by={}, true_monkey={}, false_monkey={}, inspections={}".format(
                self.items,
                self.operation,
                self.divisible_by,
                self.true_monkey,
                self.false_monkey, self.inspections))


def get_monkeys(monkeys):
    return [Monkey(m) for m in monkeys]


def run_round(monkeys, divide_by_3, common_mod):
    for monkey in monkeys:
        for item in monkey.items:
            old = item
            worry = eval(monkey.operation)

            if divide_by_3:
                worry //= 3
            worry %= common_mod
            if worry % monkey.divisible_by == 0:
                monkeys[monkey.true_monkey].items.append(worry)
            else:
                monkeys[monkey.false_monkey].items.append(worry)

        monkey.inspections += len(monkey.items)
        monkey.items = []
    return monkeys


# print(monkeys)

def run_rounds(times, monkeys, divide_by_3):
    common_mod = math.prod([m.divisible_by for m in monkeys])
    for _ in range(1, times + 1):
        monkeys = run_round(monkeys, divide_by_3, common_mod)
    return monkeys


monkeys = get_monkeys(data)
monkeys = run_rounds(20, monkeys, True)
monkeys.sort(key=lambda x: x.inspections, reverse=True)
part1 = monkeys[0].inspections * monkeys[1].inspections
assert part1 == 57348  # Input
print("Part 1:", part1)

monkeys = get_monkeys(data)
monkeys = run_rounds(10000, monkeys, False)
monkeys.sort(key=lambda x: x.inspections, reverse=True)
part2 = monkeys[0].inspections * monkeys[1].inspections
assert part2 == 14106266886
print("Part 2:", part2)
