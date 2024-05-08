import numpy as np


class Lagoon:

    MOVES = {
        'U': np.array([-1, 0]),
        'D': np.array([1, 0]),
        'L': np.array([0, -1]),
        'R': np.array([0, 1]),
    }

    CONVERSION = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U',
    }

    def __init__(self, part: int):
        self.directions, self.steps = self.parse_input(part)

    def parse_input(self, part: int) -> tuple[list[str], list[int]]:
        with open('inputs/18.txt', mode='r') as file:
            lines = file.read().splitlines()

        directions = []
        steps = []
        for line in lines:
            direction, step, color = line.split(' ')
            if part == 1:
                directions.append(direction)
                steps.append(int(step))
            else:
                color = color.replace('(', '').replace(')', '')
                directions.append(self.CONVERSION[color[-1]])
                steps.append(int(color[1:6], 16))

        return directions, steps

    def solve(self):
        """Shoelace formula + Pick's theorem."""
        coors_0 = np.array((0, 0))
        num_boundary_points = 1
        interior_area = 0

        for direction, step in zip(self.directions, self.steps):
            coors_1 = coors_0 + step * self.MOVES[direction]
            num_boundary_points += step
            interior_area += (coors_0[1] + coors_1[1]) * (coors_0[0] - coors_1[0])
            coors_0 = coors_1

        interior_area = 0.5 * abs(interior_area)
        return num_boundary_points, int(interior_area + 1 - num_boundary_points / 2)


def main():
    for part in [1, 2]:
        lagoon = Lagoon(part)
        num_boundary_points, num_interior_points = lagoon.solve()
        print(num_boundary_points + num_interior_points)


if __name__ == '__main__':
    main()
