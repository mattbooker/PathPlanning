import math

def nhood4(grid, x, y):
    result = []

    for k in range(-1,2):

        if k == 0:
            continue

        if grid.in_bounds(x + k, y) and grid[x + k, y] != 1:
            result.append((x + k, y))

        if grid.in_bounds(x, y + k) and grid[x, y + k] != 1:
            result.append((x, y + k))

    return result


def nhood8(grid, x, y):
    result = []

    for i in range(-1, 2):
        for j in range(-1, 2):

            if i == 0 and j == 0:
                continue

            if grid.in_bounds(x + i, y + j) and grid[x + i, y + j] != 1:
                result.append((x + i, y + j))

    return result

def distance(point_1, point_2):
    return math.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)
