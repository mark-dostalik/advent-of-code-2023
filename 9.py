import numpy as np


def parse_input() -> list[list[int]]:
    with open('inputs/9.txt', mode='r') as f:
        lines = f.read().splitlines()

    return [[int(char) for char in line.split()] for line in lines]


def main():
    part1, part2 = 0, 0
    for sequence in parse_input():
        process = [sequence]
        while True:
            differences = np.diff(sequence)
            if not differences.any():
                break
            process.append(differences)
            sequence = differences

        leftmost = 0
        for s in reversed(process):
            part1 += s[-1]
            leftmost = s[0] - leftmost

        part2 += leftmost

    print(part1)
    print(part2)


if __name__ == '__main__':
    main()
