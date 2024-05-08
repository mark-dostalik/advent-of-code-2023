import itertools
import numpy as np


def main():
    universe = np.genfromtxt('inputs/11.txt', dtype=str, comments=None, delimiter=1)

    height, width = universe.shape
    galaxy_rows, galaxy_cols = np.where(universe == '#')
    missing_rows = set(range(0, height)) - set(galaxy_rows)
    missing_columns = set(range(0, width)) - set(galaxy_cols)

    part1_length = 0
    part2_length = 0
    for (row1, col1), (row2, col2) in itertools.combinations(zip(galaxy_rows, galaxy_cols), 2):
        part1_length += abs(row2 - row1) + abs(col2 - col1)
        part2_length += abs(row2 - row1) + abs(col2 - col1)
        for row in missing_rows:
            if row in range(min(row1, row2) + 1, max(row1, row2)):
                part1_length += 1
                part2_length += 1_000_000 - 1
        for col in missing_columns:
            if col in range(min(col1, col2) + 1, max(col1, col2)):
                part1_length += 1
                part2_length += 1_000_000 - 1

    print(part1_length)
    print(part2_length)


if __name__ == '__main__':
    main()
