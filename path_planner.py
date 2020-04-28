from grid import Grid
import helper as hlp
from dijkstra import Dijkstra
from astar import AStar

import random

def generate_free_point(grid : Grid, a_x, b_x, a_y, b_y):

    point = None

    while True:
        point = (random.randint(a_x, b_x), random.randint(a_y, b_y))

        if grid[point] == 0:
            break

    return point

random.seed()
map_2d = Grid(100,100)

map_2d.generate_random_map(2, 0.25, 3, 2)

# Generate start and goal point
start = generate_free_point(map_2d, 0, 0.1 * map_2d.size_x, 0, 0.1 * map_2d.size_y)
goal = generate_free_point(map_2d, 0.9 * map_2d.size_x, map_2d.size_x - 1, 0.9 * map_2d.size_y, map_2d.size_y - 1)

# # Fill in the start/goal point
map_2d[start] = 5
map_2d[goal] = 2

# dijk_planner = Dijkstra()
# path = dijk_planner.solve(map_2d, start, goal)

# dijk_planner.animate(map_2d)

astar_planner = AStar()
path = astar_planner.solve(map_2d, start, goal)

astar_planner.animate(map_2d, 50)

# for i in path:
#     map_2d[i] = 3



# map_2d.display()




