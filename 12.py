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


def check_pattern(pattern: str) -> bool:
    if not pattern:
        return False
    if '.' not in pattern[1:-1] and pattern[0] in ['?', '.', '*'] and pattern[-1] in ['?', '.', '*']:
        return True
    return False


def traverse(record: str, length: int) -> tuple[int, str]:
    if len(record) == length:
        return 0, '*' + record + '*'
    yield 0, '*' + record[:length+1]
    for index in range(len(record) - length - 1):
        yield index, record[index:index+length+2]
    yield len(record) - length - 1, record[len(record) - length - 1:len(record) + 1] + '*'


@cache
def process_record(record: str, sizes: tuple):
    if len(record) < sum(sizes):
        return 0

    if not sizes:
        if '#' not in record:
            return 1
        return 0

    if len(sizes) == 1 and len(record) == sizes[0] and '.' not in record:
        return 1

    count = 0
    size = sizes[0]
    for index, substring in traverse(record, size):
        if check_pattern(substring):
            new_record = record[index+len(substring.replace('*', '')):]
            new_sizes = sizes[1:]
            new_count = process_record(new_record, new_sizes)
            count += new_count
        if substring[0] == '#':
            break
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
