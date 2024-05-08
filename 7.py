from functools import cmp_to_key, partial

LABELS_1 = ('A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2')
LABELS_2 = ('A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J')
HAND_TYPES = ((5,), (1, 4), (2, 3), (1, 1, 3), (1, 2, 2), (1, 1, 1, 2), (1, 1, 1, 1, 1))


def parse_input() -> list[tuple[str, ...]]:
    with open('inputs/7.txt', mode='r') as f:
        lines = f.read().splitlines()

    return [tuple(line.split(' ')) for line in lines]


def get_hand_score(hand, part: int) -> int:
    label_counts = {label: hand.count(label) for label in set(hand)}

    if part == 2:
        num_jokers = label_counts.pop('J', None)

        if num_jokers == 5:
            return 0

        if num_jokers is not None:
            label_counts[max(label_counts, key=label_counts.get)] += num_jokers

    return HAND_TYPES.index(tuple(sorted(label_counts.values())))


def compare(x_hand_bid: tuple[str, str], y_hand_bid: tuple[str, str], part: int) -> int:
    x_hand, _ = x_hand_bid
    y_hand, _ = y_hand_bid

    diff = get_hand_score(y_hand, part) - get_hand_score(x_hand, part)

    if diff == 0:
        labels = LABELS_1 if part == 1 else LABELS_2
        for x_label, y_label in zip(x_hand, y_hand):
            diff = labels.index(y_label) - labels.index(x_label)
            if diff:
                return diff

    return diff


def main():
    hands_bids = parse_input()

    for part in [1, 2]:
        sorted_hands_bids = sorted(hands_bids, key=cmp_to_key(partial(compare, part=part)))
        total_winnings = 0
        for rank, (_, bid) in enumerate(sorted_hands_bids, start=1):
            total_winnings += rank * int(bid)
        print(total_winnings)


if __name__ == '__main__':
    main()
