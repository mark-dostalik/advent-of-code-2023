import re

NUMS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def get_calibration_value(line: str, part: int):
    if part == 1:
        pattern = r'\d'
    elif part == 2:
        for num, value in NUMS.items():
            line = re.sub(num, num[0] + value + num[-1], line)
        pattern = r'\d|one|two|three|four|five|six|seven|eight|nine'
    else:
        raise NotImplementedError()

    nums = re.findall(pattern, line)

    return int(NUMS.get(nums[0], nums[0]) + NUMS.get(nums[-1], nums[-1]))


def main():
    part1_sum = 0
    part2_sum = 0
    with open('inputs/1.txt', mode='r') as f:
        for line in f:
            part1_sum += get_calibration_value(line, part=1)
            part2_sum += get_calibration_value(line, part=2)

    print(part1_sum)
    print(part2_sum)


if __name__ == '__main__':
    main()
