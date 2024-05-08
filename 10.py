import numpy as np


class PipeMaze:

    PIPES = {
        '|': 'NS',
        '-': 'WE',
        'L': 'NE',
        'J': 'NW',
        '7': 'SW',
        'F': 'SE',
        '.': '',
    }
    OPPOSITES = {
        'N': 'S',
        'S': 'N',
        'W': 'E',
        'E': 'W'
    }
    MOVES = {
        'N': (-1, 0),
        'S': (1, 0),
        'W': (0, -1),
        'E': (0, 1),
    }

    def __init__(self):
        self.grid = np.genfromtxt('inputs/10.txt', dtype=str, delimiter=1)
        self.height, self.width = self.grid.shape
        self.start = np.argwhere(self.grid == 'S')[0]

    def find_start_neighbor(self) -> tuple[np.ndarray, str]:
        for direction, coors_diff in self.MOVES.items():
            y, x = self.start + coors_diff
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.OPPOSITES[direction] in self.PIPES[self.grid[y, x]]:
                    return np.array((y, x)), self.OPPOSITES[direction]

    def move(self, coors: np.ndarray, previous: str) -> tuple[np.ndarray, str]:
        direction = self.PIPES[self.grid[*coors]].replace(previous, '')
        return coors + self.MOVES[direction], self.OPPOSITES[direction]

    def solve(self) -> tuple[int, int]:
        """Shoelace formula + Pick's theorem."""
        coors_0, previous_0 = self.find_start_neighbor()
        interior_area = (self.start[1] + coors_0[1]) * (self.start[0] - coors_0[0])
        num_boundary_points = 1

        while not np.all(coors_0 == self.start):
            coors_1, previous_1 = self.move(coors_0, previous_0)
            interior_area += (coors_0[1] + coors_1[1]) * (coors_0[0] - coors_1[0])
            num_boundary_points += 1
            coors_0, previous_0 = coors_1, previous_1

        interior_area = 0.5 * abs(interior_area)
        return num_boundary_points, int(interior_area + 1 - num_boundary_points / 2)


def main():
    grid = PipeMaze()
    num_boundary_points, num_interior_points = grid.solve()
    print(num_boundary_points // 2)
    print(num_interior_points)


if __name__ == '__main__':
    main()
