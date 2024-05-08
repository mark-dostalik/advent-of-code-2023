import numpy as np


def tilt_north(platform: np.ndarray) -> None:
    for col in range(platform.shape[1]):
        moving_parts = ''.join(platform[:, col]).split('#')
        platform[:, col] = np.array(list('#'.join([''.join(sorted(part, reverse=True)) for part in moving_parts])))


def get_score(platform: np.ndarray) -> int:
    return np.sum(np.arange(platform.shape[0], 0, -1) @ (platform == 'O'))


def main():
    platform = np.genfromtxt('inputs/14.txt', dtype=str, comments=None, delimiter=1)
    scores = {0: get_score(platform)}
    hashes = {hash(platform.data.tobytes()): 0}
    total_cycles = 1_000_000_000

    i = 0
    while i < total_cycles:
        for k in range(4):
            tilt_north(np.rot90(platform, 4 - k))
            if i == 0 and k == 0:
                print(get_score(platform))
        i += 1
        current = hash(platform.data.tobytes())
        if current in hashes:
            break
        hashes[current] = i
        scores[i] = get_score(platform)

    start = hashes[current]
    period = i - start
    print(scores[start + (total_cycles - start) % period])


if __name__ == '__main__':
    main()
