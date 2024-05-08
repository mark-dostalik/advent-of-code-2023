import itertools
import math


def parse_input(part: int) -> tuple[str, list[str], dict[str, tuple[str, str]]]:
    with open('inputs/8.txt', mode='r') as f:
        lines = f.read().splitlines()

    origins = ['AAA'] if part == 1 else []
    mappings = dict()
    for line in lines[2:]:
        origin, dest = line.split(' = ')
        if part == 2 and origin[-1] == 'A':
            origins.append(origin)
        dest_left, dest_right = dest.split(', ')
        mappings[origin] = (dest_left[1:], dest_right[:-1])

    return lines[0], origins, mappings


def get_num_steps(moves: str, origins: list[str], mappings: dict[str, tuple[str, str]]):
    cycles = []
    for origin in origins:
        move_count = 1
        for move in itertools.cycle(0 if move == 'L' else 1 for move in moves):
            origin = mappings[origin][move]
            if origin[-1] == 'Z':
                cycles.append(move_count)
                break
            move_count += 1

    return math.lcm(*cycles)


def main():
    for part in [1, 2]:
        moves, origins, mappings = parse_input(part=part)
        num_steps = get_num_steps(moves, origins, mappings)
        print(num_steps)


if __name__ == '__main__':
    main()
