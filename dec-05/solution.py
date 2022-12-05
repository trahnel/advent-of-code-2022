# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = f.read()


# print(data)


def get_crates(all_data):
    crate_data = [[line[i] for i in range(1, len(line), 4)] for line in
                  all_data.split('\n 1')[0].split('\n')]

    # Pivot data
    c = list(map(list, zip(*reversed(crate_data))))
    c = [list(filter(lambda x: x != ' ', line)) for line in c]
    return c


# [1, 2, 3] => move 1 from 2 to 3
def get_moves(all_data):
    return [tuple(int(i) for i in x.split() if i.isdigit()) for x in all_data.split('\n\n')[1].split('\n')]


def move_crane(crates, moves, reverse=False):
    for move in moves:
        count = move[0]
        frm = move[1] - 1
        to = move[2] - 1

        if reverse:
            to_move = list(reversed(crates[frm][-count:]))
        else:
            to_move = list(crates[frm][-count:])
        del crates[frm][-count:]
        crates[to].extend(to_move)
    return crates


moves = get_moves(data)
print(moves)

crates = get_crates(data)
print(crates)
crates = move_crane(crates, moves, reverse=True)

part1 = ''.join([x.pop() for x in crates])
assert part1 == 'QMBMJDFTD'
print('Part1: ', part1)

crates = get_crates(data)
crates = move_crane(crates, moves, reverse=False)

part2 = ''.join([x.pop() for x in crates])
assert part2 == 'NBTVTJNFJ'
print('Part2: ', part2)
