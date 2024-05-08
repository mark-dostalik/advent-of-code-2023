import math


def parse_input() -> tuple[list[int], list[int]]:
    with open('inputs/6.txt', mode='r') as f:
        lines = f.read().splitlines()

    _, durations = lines[0].split(':')
    _, distances = lines[1].split(':')

    durations = [int(d) for d in durations.split()]
    distances = [int(d) for d in distances.split()]

    return durations, distances


def count_ways(duration: int, record: int) -> int:
    t_min = max(0, math.floor(0.5 * (duration - math.sqrt(duration ** 2 - 4 * record)) + 1))
    t_max = min(duration, math.ceil(0.5 * (duration + math.sqrt(duration ** 2 - 4 * record)) - 1))
    return t_max - t_min + 1


def main():
    durations, records = parse_input()
    full_duration, full_record = int(''.join(str(d) for d in durations)), int(''.join(str(r) for r in records))

    part1 = 1
    for duration, record in zip(durations, records):
        part1 *= count_ways(duration, record)

    print(part1)
    print(count_ways(full_duration, full_record))


if __name__ == '__main__':
    main()
