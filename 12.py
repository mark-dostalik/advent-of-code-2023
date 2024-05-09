from functools import cache


def parse_input(part: int) -> tuple[list[str], list[tuple[int, ...]]]:
    with open('inputs/12.txt', mode='r') as f:
        lines = f.read().splitlines()

    records = []
    sizes = []
    for line in lines:
        record, nums_raw = line.split(' ')
        record = 4 * (record + '?') + record if part == 2 else record
        nums = [int(num) for num in nums_raw.split(',')]
        nums = 5 * nums if part == 2 else nums

        records.append(record)
        sizes.append(tuple(nums))

    return records, sizes


def check_record(record: str, size: int) -> bool:
    return len(record) >= size and '.' not in record[:size] and (len(record) == size or record[size] != '#')


@cache
def process_record(record: str, sizes: tuple[int]) -> int:
    if not record:
        return len(sizes) == 0

    if not sizes:
        return '#' not in record

    count = 0

    if record[0] in '.?':
        count += process_record(record[1:], sizes)

    if record[0] in '#?' and check_record(record, sizes[0]):
        count += process_record(record[sizes[0] + 1:], sizes[1:])

    return count


def main():
    for part in [1, 2]:
        total = 0
        records, sizes = parse_input(part)
        for record, sizes in zip(records, sizes):
            total += process_record(record, sizes)
        print(total)


if __name__ == '__main__':
    main()
