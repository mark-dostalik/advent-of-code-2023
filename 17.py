import queue
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, order=True)
class Node:
    coors: tuple[int, int]
    direction: str
    num_steps: int
    distance: int


class City:

    MOVES = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1),
    }

    OPPOSITES = {
        'U': 'D',
        'D': 'U',
        'L': 'R',
        'R': 'L',
    }

    PERPENDICULAR = {
        'U': 'LR',
        'D': 'LR',
        'L': 'UD',
        'R': 'UD',
        'start': 'RD',
    }

    def __init__(self):
        graph = np.genfromtxt('inputs/17.txt', dtype=int, delimiter=1)
        height, width = graph.shape

        self.graph = graph
        self.start = (0, 0)
        self.end = (height - 1, width - 1)

    @staticmethod
    def manhattan_distance(coors_1: tuple[int, int], coors_2: tuple[int, int]) -> int:
        y_1, x_1 = coors_1
        y_2, x_2 = coors_2
        return abs(x_1 - x_2) + abs(y_1 + y_2)

    def check_coors(self, coors) -> bool:
        height, width = self.graph.shape
        y, x = coors
        return 0 <= y < height and 0 <= x < width

    def get_distance(self, source: tuple[int, int], target: tuple[int, int]) -> int:
        y_0, x_0 = source
        y, x = target
        if y > y_0:
            return np.sum(self.graph[y_0 + 1: y + 1, x_0])
        if y_0 > y:
            return np.sum(self.graph[y: y_0, x_0])
        if x > x_0:
            return np.sum(self.graph[y_0, x_0 + 1: x + 1])
        return np.sum(self.graph[y_0, x: x_0])

    def new_neighbor(self, node: Node, coors_diff: tuple[int, int], direction: str, num_steps: int) -> list[Node]:
        y_curr, x_curr = node.coors
        y_diff, x_diff = coors_diff
        y, x = y_curr + num_steps * y_diff, x_curr + num_steps * x_diff
        if self.check_coors((y, x)):
            distance = self.get_distance(node.coors, (y, x))
            if node.direction == direction:
                return [Node((y, x), direction, node.num_steps + num_steps, distance)]
            return [Node((y, x), direction, num_steps, distance)]
        return []

    def get_neighbors(self, node: Node, min_steps: int, max_steps: int) -> list[Node]:
        neighbors = []

        for direction, coors_diff in self.MOVES.items():
            if direction in self.PERPENDICULAR[node.direction]:
                neighbors += self.new_neighbor(node, coors_diff, direction, min_steps)
                continue
            if node.num_steps == max_steps and node.direction == direction:
                continue
            if not direction == self.OPPOSITES.get(node.direction):
                neighbors += self.new_neighbor(node, coors_diff, direction, 1)

        return neighbors

    def solve(self, min_steps: int, max_steps: int) -> int:
        assert 1 <= min_steps < max_steps
        frontier = queue.PriorityQueue()
        frontier.put((0, Node(self.start, 'start', 0, 0)))
        cost_so_far = {Node(self.start, 'start', 0, 0): 0}
        came_from = {Node(self.start, 'start', 0, 0): None}

        while not frontier.empty():
            _, current = frontier.get()

            if current.coors == self.end:
                return cost_so_far[current]

            for neighbor in self.get_neighbors(current, min_steps=min_steps, max_steps=max_steps):
                distance = cost_so_far[current] + neighbor.distance
                if neighbor not in cost_so_far or distance < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = distance
                    came_from[neighbor] = current
                    frontier.put((distance + self.manhattan_distance(current.coors, self.end), neighbor))


def main():
    city = City()
    print(city.solve(min_steps=1, max_steps=3))
    print(city.solve(min_steps=4, max_steps=10))


if __name__ == '__main__':
    main()
