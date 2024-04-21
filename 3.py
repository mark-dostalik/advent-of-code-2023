import re


def process_line_part1(row: int, line: str, lines: list[str]) -> int:
    height, width = len(lines), len(lines[0])
    ret = 0

    for match in re.finditer(r'\d+', line):
        found = False
        for x in range(match.start() - 1, match.end() + 1):
            if found:
                break
            if x < 0 or x >= width:
                continue
            for y in [row - 1, row, row + 1]:
                if y < 0 or y >= height:
                    continue
                if not lines[y][x].isdigit() and lines[y][x] != '.':
                    found = True
                    ret += int(match.group(0))

    return ret


def process_line_part2(row: int, line: str, lines: list[str]) -> int:
    height, width = len(lines), len(lines[0])
    ret = 0

    for asterisk_match in re.finditer(r'\*', line):
        found = []
        asterisk_x_range = range(asterisk_match.start() - 1, asterisk_match.end() + 1)
        for y in [row - 1, row, row + 1]:
            if y < 0 or y >= height:
                continue
            for digit_match in re.finditer(r'\d+', lines[y]):
                if set(range(digit_match.start(), digit_match.end())) & set(asterisk_x_range):
                    found.append(int(digit_match.group(0)))
        if len(found) == 2:
            ret += found[0] * found[1]

    return ret


def main():
    with open('inputs/3.txt', mode='r') as f:
        lines = f.read().splitlines()

    part1_sum = 0
    part2_sum = 0

    for row, line in enumerate(lines):
        part1_sum += process_line_part1(row, line, lines)
        part2_sum += process_line_part2(row, line, lines)

    print(part1_sum)
    print(part2_sum)


if __name__ == '__main__':
    main()
