from collections import defaultdict


def parse_input() -> list[str]:
    with open('inputs/15.txt', mode='r') as file:
        line = file.read().splitlines()[0]
    return line.split(',')


def hash_string(string: str) -> int:
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def main():
    part1 = 0
    part2 = 0

    boxes: dict[int, dict[str, int]] = defaultdict(dict)  # dict preserves insertion order in Python >= 3.6

    for string in parse_input():
        part1 += hash_string(string)

        if '=' in string:
            lens, focal_length = string.split('=')
            boxes[hash_string(lens)][lens] = int(focal_length)
        elif '-' in string:
            lens, _ = string.split('-')
            boxes[hash_string(lens)].pop(lens, None)
        else:
            raise ValueError(f'Unknown pattern: {string}.')

    for box_number, box_content in boxes.items():
        box_total = 0
        for order, focal_length in enumerate(box_content.values()):
            box_total += (box_number + 1) * (order + 1) * focal_length
        part2 += box_total

    print(part1)
    print(part2)


if __name__ == '__main__':
    main()
