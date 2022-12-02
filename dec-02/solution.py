# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = f.readlines()

rounds = [tuple(line.strip().split()) for line in data]

# print(rounds)

shape_score = {
    'R': 1,  # ROCK
    'P': 2,  # PAPER
    'S': 3  # SCISSORS
}


def get_outcome_score(opp, me):
    # DRAW
    if opp == me:
        return 3
    # WIN
    if opp == 'R' and me == 'P' \
            or opp == 'P' and me == 'S' \
            or opp == 'S' and me == 'R':
        return 6
    # LOST
    else:
        return 0


def get_hand(hand):
    if hand in ['A', 'X']:
        return 'R'  # ROCK
    elif hand in ['B', 'Y']:
        return 'P'  # PAPER
    elif hand in ['C', 'Z']:
        return 'S'  # SCISSORS


part1 = 0
for hands in rounds:
    opp = get_hand(hands[0])
    me = get_hand(hands[1])
    part1 += shape_score[me] + get_outcome_score(opp, me)

assert part1 == 8890
print('Part 1:', part1)


# Y = DRAW
# X = LOSE
# Z = WIN
def get_my_hand(opp, outcome):
    # DRAW
    if outcome == 'Y':
        return opp
    # WIN
    elif outcome == 'Z':
        if opp == 'R':
            return 'P'
        elif opp == 'P':
            return 'S'
        elif opp == 'S':
            return 'R'
    # LOSE
    elif outcome == 'X':
        if opp == 'R':
            return 'S'
        elif opp == 'P':
            return 'R'
        elif opp == 'S':
            return 'P'


part2 = 0
for hands in rounds:
    opp = get_hand(hands[0])
    outcome = hands[1]
    me = get_my_hand(opp, outcome)
    part2 += shape_score[me] + get_outcome_score(opp, me)

assert part2 == 10238
print('Part 2:', part2)
