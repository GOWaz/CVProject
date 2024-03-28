import numpy as np
import matplotlib.pyplot as plt

class Cutter:
    def __init__(self):
        pass

    def cut_image_into_grid(self, image, num_rows, num_cols):
        row_ranges = self._calculate_ranges(image.shape[0], num_rows)
        col_ranges = self._calculate_ranges(image.shape[1], num_cols)
        print(f'ww {row_ranges} hh {col_ranges}')
        grid = [image[j:jj, i:ii, :] for j, jj in row_ranges for i, ii in col_ranges]
        return grid, len(row_ranges), len(col_ranges)

    def display_grid(self, grid, num_rows, num_cols,title="", figure_height=10, figure_width=10):
        fig, ax = plt.subplots(nrows=num_rows, ncols=num_cols)
        [axi.set_axis_off() for axi in ax.ravel()]
        fig.suptitle(title, fontsize=16)
        fig.set_figheight(figure_height)
        fig.set_figwidth(figure_width)

        c = 0
        for row in ax:
            for col in row:
                col.imshow(np.flip(grid[c], axis=-1))
                c += 1

        plt.draw()
        plt.pause(0.001)  # Adjust the pause duration as needed

    def cut_and_shuffle(self, image, num_rows, num_cols):
        grid, rows, cols = self.cut_image_into_grid(image, num_rows, num_cols)
        np.random.shuffle(grid)
        return grid, rows, cols

    def _calculate_ranges(self, length, num_sections):
        return [[i.min(), i.max()] for i in np.array_split(range(length), num_sections)]



# cutter = Cutter()
#
# image_to_cut = plt.imread('../Asset/1.jpg')
# cut_grid, rows, cols = cutter.cut_and_shuffle(image_to_cut, 6, 20)
# cutter.display_grid(cut_grid, rows, cols)
