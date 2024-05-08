import itertools

Mapping = tuple[int, int, int]


def parse_line(line: str) -> Mapping:
    dest_start, source_start, size = [int(num) for num in line.split()]
    return dest_start, source_start, size


def parse_block(block: str) -> list[Mapping]:
    return [parse_line(line) for line in block.split('\n')[1:]]


def parse_input() -> tuple[list[int], list[list[Mapping]]]:
    with open('inputs/5.txt', mode='r') as f:
        blocks = f.read().split('\n\n')

    _, seeds = blocks[0].split(':')
    seeds = [int(num) for num in seeds.split()]
    mapping_blocks = [parse_block(block) for block in blocks[1:]]

    return seeds, mapping_blocks


def transform(
        start: int,
        end: int,
        mappings: list[Mapping],
        seed_ranges: list[tuple[int, int]],
        transformed_seed_ranges: list[tuple[int, int]]
) -> None:
    for dest_start, source_start, size in mappings:
        intersection_start = max(source_start, start)
        intersection_end = min(source_start + size, end)

        if intersection_start < intersection_end:
            transformed_seed_ranges.append(
                (
                    dest_start + intersection_start - source_start,
                    dest_start + intersection_end - source_start,
                )
            )

            if start < intersection_start:
                seed_ranges.append((start, intersection_start))

            if intersection_end < end:
                seed_ranges.append((intersection_end, end))

            return

    transformed_seed_ranges.append((start, end))
    return


def main():
    seeds, mapping_blocks = parse_input()

    for part in [1, 2]:
        if part == 1:
            seed_ranges = [(start, start + 1) for start in seeds]
        else:
            seed_ranges = [(start, start + size) for start, size in itertools.batched(seeds, 2)]

        for mappings in mapping_blocks:
            transformed_seed_ranges = []
            while seed_ranges:
                start, end = seed_ranges.pop()
                transform(start, end, mappings, seed_ranges, transformed_seed_ranges)

            seed_ranges = transformed_seed_ranges

        print(min(seed_ranges)[0])


if __name__ == '__main__':
    main()
