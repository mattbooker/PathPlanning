import helper as hlp
from collections import defaultdict
import heapq as h

class AStar:

    def __init__(self):
        self._animate_visited = []

    def solve(self, grid, start, goal):
        visited = set()
        prev = dict()
        dist = defaultdict(lambda : float('inf'))
        pq = []

        prev[start] = None
        dist[start] = 0

        # Need to put (cost, pos) into priority queue so that pq is ordered by cost
        h.heappush(pq, (0, start))

        while len(pq) != 0:

            current_cost, current_pos = h.heappop(pq)

            self._animate_visited.append(current_pos)

            # Check we havent visited this point before
            if current_pos not in visited:
                visited.add(current_pos)
            else:
                continue
            
            # If we have reached the end get the path
            if current_pos == goal:
                return self.get_path(prev, goal)

            # print(pq)

            for nbr in hlp.nhood8(grid, *current_pos):
                new_cost = dist[current_pos] + hlp.distance(current_pos, nbr)
                heuristic = hlp.distance(nbr, goal)

                # If we havent visited
                if nbr not in visited:

                    if new_cost < dist[nbr]:
                        dist[nbr] = new_cost
                        prev[nbr] = current_pos

                    h.heappush(pq, (dist[nbr] + heuristic, nbr))

    def get_path(self, prev, goal):
        
        self.path = []

        current_pos = goal
        
        # Extract path from goal to start (start is the only item that has none associated with it in prev)
        while prev[current_pos] != None:
            current_pos = prev[current_pos]
            self.path.append(current_pos)

        # Return path reveresed and remove start node
        return self.path[:-1:-1]

    def animate(self, grid, cells_at_once=50):

        # Remove start and end points
        grid.animate(self._animate_visited[1:-1], self.path, cells_at_once)


                        


