from dataclasses import dataclass
from functools import cache

import numpy as np


@dataclass(frozen=True)
class State:
    coors: tuple[int, int]
    from_direction: str


class MirrorMaze:

    MOVES = {
        'N': (-1, 0),
        'S': (1, 0),
        'W': (0, -1),
        'E': (0, 1),
    }

    OPPOSITES = {
        'N': 'S',
        'S': 'N',
        'E': 'W',
        'W': 'E',
    }

    PIPES = {
        '|': {
            'N': 'S',
            'S': 'N',
            'E': 'NS',
            'W': 'NS',
        },
        '-': {
            'N': 'EW',
            'S': 'EW',
            'E': 'W',
            'W': 'E',
        },
        '/': {
            'N': 'W',
            'S': 'E',
            'E': 'S',
            'W': 'N',
        },
        '\\': {
            'N': 'E',
            'S': 'W',
            'E': 'N',
            'W': 'S',
        },
        '.': OPPOSITES,
    }

    def __init__(self):
        self.grid = np.genfromtxt('inputs/16.txt', dtype=str, delimiter=1)
        self.edge_states = self.generate_edge_states()

    def generate_edge_states(self) -> set[State]:
        height, width = self.grid.shape
        edge_states = set()
        edge_states |= {State(coors=(0, x), from_direction='N') for x in range(0, width)}
        edge_states |= {State(coors=(height - 1, x), from_direction='S') for x in range(0, width)}
        edge_states |= {State(coors=(y, 0), from_direction='W') for y in range(0, height)}
        edge_states |= {State(coors=(y, width - 1), from_direction='E') for y in range(0, height)}
        return edge_states

    def check_coors(self, coors: tuple[int, int]) -> bool:
        y, x = coors
        height, width = self.grid.shape
        return 0 <= x < width and 0 <= y < height

    @cache
    def move(self, state: State):
        states = set()
        y_curr, x_curr = state.coors
        from_direction = state.from_direction
        for towards in self.PIPES[self.grid[state.coors]][from_direction]:
            y_diff, x_diff = self.MOVES[towards]
            y, x = y_curr + y_diff, x_curr + x_diff
            if self.check_coors((y, x)):
                states.add(State(coors=(y, x), from_direction=self.OPPOSITES[towards]))
        return states

    def count_energized(self, initial_state: State) -> tuple[int, set[State]]:
        queue = [initial_state]
        seen = set()
        while queue:
            current = queue.pop()
            if current in seen:
                continue
            seen.add(current)

            for state in self.move(current):
                if state not in seen:
                    queue.append(state)

        seen_edge_states = {s for s in self.edge_states if State(s.coors, self.OPPOSITES[s.from_direction]) in seen}

        return len({state.coors for state in seen}), seen_edge_states

    def find_highest_energy(self) -> int:
        tested_edge_states = {}
        for state in self.edge_states:
            if state not in tested_edge_states:
                num_energized, seen_edge_states = self.count_energized(state)
                for edge_state in seen_edge_states:
                    tested_edge_states[edge_state] = num_energized

        return max(tested_edge_states.values())


def main():
    mirror_maze = MirrorMaze()
    num_energized, _ = mirror_maze.count_energized(State(coors=(0, 0), from_direction='W'))
    print(num_energized)
    print(mirror_maze.find_highest_energy())


if __name__ == '__main__':
    main()
