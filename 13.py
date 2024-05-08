import numpy as np


def parse_input() -> list[np.ndarray]:
    with open('inputs/13.txt', 'r') as f:
        patterns = []
        for block in f.read().split('\n\n'):
            pattern = []
            for line in block.split('\n'):
                if line:
                    pattern.append([c == '#' for c in line])
            patterns.append(np.array(pattern, dtype=int))

    return patterns


def get_reflection_row_index(pattern: np.ndarray, diff: int) -> int:
    for i in range(pattern.shape[0] - 1):
        upper_flipped = np.flipud(pattern[:i + 1])
        lower = pattern[i + 1:]
        rows = min(upper_flipped.shape[0], lower.shape[0])
        if np.count_nonzero(upper_flipped[:rows] - lower[:rows]) == diff:
            return i + 1
    return 0


def main():
    patterns = parse_input()

    for diff in [0, 1]:
        total = 0
        for pattern in patterns:
            total += 100 * get_reflection_row_index(pattern, diff) + get_reflection_row_index(pattern.T, diff)
        print(total)


if __name__ == '__main__':
    main()
