import random

import matplotlib as mpl
import numpy as np
from matplotlib import animation as ani
from matplotlib import pyplot as plt

class Grid:

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self._grid = np.zeros((self.size_x, self.size_y))

        random.seed(56)

    def display(self):
        
        # matplotlib will get very slow for over 100x100 grid cells
        plt.figure(figsize=(self.size_x, self.size_y))
        cmap = plt.cm.hsv  # define the colormap

        # Take 8 colors
        cmaplist = [cmap(i) for i in range(0,256,32)]

        # Make the first two entries white, black
        cmaplist = [(1, 1, 1, 1.0), (0, 0, 0, 1.0)] + cmaplist

        # create the new map
        cmap = mpl.colors.LinearSegmentedColormap.from_list(
            'Custom cmap', cmaplist, 10)

        # define the bins and normalize
        bounds = np.linspace(0, 9, 10)
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

        plt.pcolormesh(self._grid, cmap=cmap, norm=norm)
        ax = plt.gca()
        ax.set_aspect(1)
        plt.colorbar()

        plt.show()       

    def animate(self, visited_cells, final_path, cells_at_once):
        fig = plt.figure(figsize=(10, 10))
        grid_copy = self._grid.copy()

        cmap = plt.cm.hsv  # define the colormap

        # Take 8 colors
        cmaplist = [cmap(i) for i in range(0,256,32)]

        # Make the first two entries white, black
        cmaplist = [(1, 1, 1, 1.0), (0, 0, 0, 1.0)] + cmaplist

        # create the new map
        cmap = mpl.colors.LinearSegmentedColormap.from_list(
            'Custom cmap', cmaplist, 10)

        # define the bins and normalize
        bounds = np.linspace(0, 9, 10)
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

        quad = plt.pcolormesh(self._grid, cmap=cmap, norm=norm)
        ax = plt.gca()
        ax.set_aspect(1)
        
        def update(grouped_cells):

            cells, color = grouped_cells

            for cell in cells:
                grid_copy[cell] = color
            quad.set_array(grid_copy.ravel())
            return quad

        grouped_cells = [(visited_cells[i:i + cells_at_once], 3) for i in range(0, len(visited_cells), cells_at_once)]
        grouped_cells.append((final_path, 5))

        final_ani = ani.FuncAnimation(fig, update, frames=grouped_cells, interval=50)
        plt.show()

        # final_ani.save('animated.gif', writer='imagemagick')

    def in_bounds(self, x, y):
        if x < 0 or x >= self.size_x or y < 0 or y >= self.size_y:
            return False
        else:
            return True

    def __getitem__(self, key):
        if self.in_bounds(key[0], key[1]):
            return self._grid[key[0], key[1]]
        else:
            raise IndexError(key[0], key[1])

    def __setitem__(self, key, value):
        if self.in_bounds(key[0], key[1]):
            self._grid[key[0], key[1]] = value
        else:
            raise IndexError(key[0], key[1])
        
    def __str__(self):
        result = ""
        for i in range(self.size_x):
            for j in range(self.size_y):
                result += str(self._grid[i, j])
                result += ', '
            result += '\n'

        return result

    '''
    Use cellular automata to generate a random map
    Adapted from 'https://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664'
    '''
    def generate_random_map(self, number_of_steps, initial_chance, birth_limit, death_limit):
        # Initialize
        for i in range(self.size_x):
            for j in range(self.size_y):
                p = random.random()

                if p < initial_chance:
                    self._grid[i, j] = 1

        # Start running the cellular automata
        for n in range(number_of_steps):
            self._grid = self._cellular_automata_step(birth_limit, death_limit)
    
    def _cellular_automata_step(self, birth_limit, death_limit):
        new_grid = np.zeros((self.size_y, self.size_x))

        for i in range(self.size_x):
            for j in range(self.size_y):
                nbs_count = self._count_nbr(i, j)

                if self._grid[i, j] == 1:
                    if nbs_count < death_limit:
                        new_grid[i, j] = 0
                    else:
                        new_grid[i, j] = 1
                else:
                    if nbs_count > birth_limit:
                        new_grid[i, j] = 1
                    else:
                        new_grid[i, j] = 0

        return new_grid

    def _count_nbr(self, x, y):

        count = 0

        for i in range(-1, 2):
            for j in range(-1, 2):

                nbr_x = x + i
                nbr_y = y + j

                # Skip
                if i == 0 and j == 0:
                    continue

                # If we off the map or found a block then add 1
                if not self.in_bounds(x+i, y+j) or self._grid[x+i, y+j] == 1:
                    count += 1

        return count
