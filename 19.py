import math
from dataclasses import dataclass

Part = tuple[int, int, int, int]


@dataclass
class Rule:
    condition: str
    destination: str


class Aplenty:

    def __init__(self):
        self.workflows, self.parts = self.parse_input()

    @staticmethod
    def parse_input() -> tuple[dict[str, list[Rule]], list[Part]]:
        with open('inputs/19.txt', mode='r') as file:
            blocks = file.read().split('\n\n')

        workflows = {}
        for line in blocks[0].split('\n'):
            rules = []
            name, rest = line.split('{')
            for item in rest[:-1].split(','):
                try:
                    condition, destination = item.split(':')
                except ValueError:
                    condition, destination = 'True', item
                rules.append(Rule(condition, destination))
            workflows[name] = rules

        parts = []
        for line in blocks[1].split('\n'):
            parts.append(tuple([int(entry.split('=')[1]) for entry in line[1:-1].split(',')]))

        return workflows, parts

    def evaluate_part(self, part: Part) -> int:
        x, m, a, s = part
        name = 'in'
        while True:
            if name == 'A':
                return x + m + a + s
            if name == 'R':
                return 0
            for rule in self.workflows[name]:
                if eval(rule.condition):
                    name = rule.destination
                    break

    def count_accepted(self, current: str, ranges: dict[str, range]) -> int:
        if current == 'R':
            return 0
        if current == 'A':
            return math.prod([r.stop - r.start for r in ranges.values()])

        total = 0
        for rule in self.workflows[current]:
            if rule.condition == 'True':
                total += self.count_accepted(rule.destination, ranges)
            else:
                variable, operator, *value = rule.condition
                value = int(''.join(value))
                new_ranges = dict(ranges)
                if ranges[variable].start < value < ranges[variable].stop:
                    if operator == '<':
                        new_ranges[variable] = range(ranges[variable].start, value)
                        ranges[variable] = range(value, ranges[variable].stop)
                    else:
                        new_ranges[variable] = range(value + 1, ranges[variable].stop)
                        ranges[variable] = range(ranges[variable].start, value + 1)

                total += self.count_accepted(rule.destination, new_ranges)

        return total


def main():
    aplenty = Aplenty()
    print(sum(aplenty.evaluate_part(part) for part in aplenty.parts))
    print(aplenty.count_accepted('in', dict(zip('xmas', (range(1, 4001) for _ in range(4))))))


if __name__ == '__main__':
    main()
