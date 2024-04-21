BOUNDS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def parse_line(line: str) -> (int, list[dict[str, int]]):
    game_id, marbles = line.split(':')
    game_id = int(game_id.replace('Game ', ''))
    draws = []

    for revealed in marbles.split(';'):
        draw = {'red': 0, 'green': 0, 'blue': 0}
        for entry in revealed.split(','):
            for name in BOUNDS:
                if name in entry:
                    draw[name] += int(entry.replace(name, '').strip())
        draws.append(draw)

    return game_id, draws


def main():
    part1_sum = 0
    part2_sum = 0
    with open('inputs/2.txt', mode='r') as f:
        for line in f:
            game_id, draws = parse_line(line)

            if all(all(count <= BOUNDS[name] for name, count in draw.items()) for draw in draws):
                part1_sum += game_id

            power = 1
            for counts in zip(*(draw.values() for draw in draws)):
                power *= max(counts)
            part2_sum += power

    print(part1_sum)
    print(part2_sum)


if __name__ == '__main__':
    main()
