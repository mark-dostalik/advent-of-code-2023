def get_num_matches(line: str) -> int:
    _, nums = line.split(':')
    winning_nums, given_nums = nums.split('|')
    return len(set(winning_nums.split()) & set(given_nums.split()))


def main():
    with open('inputs/4.txt', mode='r') as f:
        lines = f.read().splitlines()

    part1_sum = 0
    part2_sum = 0
    card_counts = len(lines) * [1]

    for index, line in enumerate(lines):
        num_matches = get_num_matches(line)

        if num_matches:
            part1_sum += 2 ** (num_matches - 1)

        part2_sum += card_counts[index]
        for k in range(index + 1, min(index + num_matches + 1, len(lines))):
            card_counts[k] += card_counts[index]

    print(part1_sum)
    print(part2_sum)


if __name__ == '__main__':
    main()
