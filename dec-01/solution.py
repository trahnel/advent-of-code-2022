# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = f.readlines()

clean = [line.strip() for line in data]
# print(clean)


i = 0
tot_cals = [0]
for _, cals in enumerate(clean):
    if not cals:
        i += 1
        tot_cals.append(0)
        continue

    tot_cals[i] += int(cals)

# assert max == 24000
tot_cals.sort(reverse=True)
# print(tot_cals)

print('Part1:', max(tot_cals))
print('Part2:', sum(tot_cals[:3]))
