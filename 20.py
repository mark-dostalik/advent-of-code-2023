import math
import queue
from collections import Counter
from dataclasses import dataclass


@dataclass
class FlipFlop:
    destinations: list[str]
    state: bool


@dataclass
class Conjunction:
    destinations: list[str]
    memory: dict[str, bool]


class System:

    def __init__(self):
        self.initial_destinations, self.modules = self.parse_input()
        self.children = dict(
            zip(
                self.initial_destinations,
                [self.get_children(name, set()) for name in self.initial_destinations]
            )
        )

    def parse_input(self) -> tuple[list[str], dict[str, FlipFlop | Conjunction]]:
        with open('inputs/20.txt', mode='r') as file:
            lines = file.read().splitlines()

        initial_destinations = []
        modules = {}
        for line in lines:
            module, destinations = line.split(' -> ')
            destinations = destinations.split(', ')
            if module == 'broadcaster':
                initial_destinations = destinations
            elif module[0] == '%':
                modules[module[1:]] = FlipFlop(destinations=destinations, state=False)
            elif module[0] == '&':
                modules[module[1:]] = Conjunction(destinations=destinations, memory={})
            else:
                raise NotImplementedError('Unknown module.')

        for module_name, module in modules.items():
            for destination in module.destinations:
                if isinstance(modules.get(destination), Conjunction):
                    modules[destination].memory[module_name] = False

        return initial_destinations, modules

    def get_children(self, name: str, children: set[str]) -> set[str]:
        if self.modules.get(name) is None:
            return children | {name}

        destinations = set(self.modules[name].destinations)
        unseen = destinations - children
        children |= destinations

        if not unseen:
            return children

        for child in unseen:
            children |= self.get_children(child, children)

        return children

    def push_button(self, pulse_count: Counter) -> Counter:
        pulse_count[False] += 1
        process = queue.Queue()
        for destination in self.initial_destinations:
            process.put((False, 'broadcaster', destination))

        while not process.empty():
            pulse, origin, destination = process.get()
            pulse_count[pulse] += 1

            destination_module = self.modules.get(destination)
            if isinstance(destination_module, FlipFlop):
                if not pulse:
                    for new_destination in destination_module.destinations:
                        process.put((not destination_module.state, destination, new_destination))
                    destination_module.state = not destination_module.state
            elif isinstance(destination_module, Conjunction):
                destination_module.memory[origin] = pulse
                for new_destination in destination_module.destinations:
                    process.put((not all(destination_module.memory.values()), destination, new_destination))

        return pulse_count

    def get_pulse_product(self, total_pushes: int) -> int:
        pulse_count = Counter()
        for _ in range(total_pushes):
            pulse_count = self.push_button(pulse_count)

        return pulse_count[True] * pulse_count[False]

    def hash_states(self, parent: str) -> int:
        return hash(
            {name: module for name, module in self.modules.items() if name in self.children[parent]}.__repr__()
        )

    def count_presses_to_deliver(self) -> int:
        cycles = dict(zip(self.initial_destinations, [0, 0, 0, 0]))
        hashed_states = {parent: [self.hash_states(parent)] for parent in self.initial_destinations}

        num_presses = 0
        while not all(cycles.values()):
            self.push_button(Counter())
            num_presses += 1
            for parent in self.initial_destinations:
                if cycles[parent]:
                    continue
                check = self.hash_states(parent)
                if check in hashed_states[parent]:
                    cycles[parent] = num_presses - hashed_states[parent].index(check)
                else:
                    hashed_states[parent].append(check)

        return math.lcm(*(cycles.values()))


def main():
    system = System()
    print(system.get_pulse_product(1000))
    print(system.count_presses_to_deliver())


if __name__ == '__main__':
    main()
