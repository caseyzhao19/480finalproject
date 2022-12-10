import copy
import math
import numpy as np

class Diagrameaux:
    def __init__(self, vals):
        values = np.copy(vals)
        num_rows, num_cols = np.shape(values)

        # cleans out empty rows and cols
        row = 0
        while row < num_rows:
            if not np.any(values[row, :]):
                values = np.delete(values, row, axis=0)
                num_rows -= 1
            else:
                row += 1

        col = 0
        while col < num_cols:
            if not np.any(values[:, col]):
                values = np.delete(values, col, axis=1)
                num_cols -= 1
            else:
                col += 1

        self.values = values

    def num_rows(self):
        return np.shape(self.values)[0]

    def num_cols(self):
        return np.shape(self.values)[1]

    def __copy__(self):
        return Diagrameaux(self.values)

    # is the row you want to move up, zero indexed
    def row_up(self, row):
        mod = copy.copy(self)
        if row == 0:
            return
        for col in range(mod.num_cols()):
            if mod.values[row - 1][col] == 0:
                mod.values[row - 1][col] = mod.values[row][col]
                mod.values[row][col] = 0
        return copy.copy(mod)

    # is the col you want to move to the left, zero indexed
    def col_left(self, col):
        mod = copy.copy(self)
        if col == 0:
            return
        for row in range(mod.num_rows()):
            if mod.values[row][col - 1] == 0:
                mod.values[row][col - 1] = mod.values[row][col]
                mod.values[row][col] = 0
        return copy.copy(mod)

    def is_tabloid(self):
        max_cols = [np.max(np.nonzero(self.values[row, :])) + 1
                    for row in range(self.num_rows())]
        max_cols_sum = sum(max_cols)
        total_num_boxes = np.count_nonzero(self.values)
        return (max_cols_sum == total_num_boxes) and np.all(np.diff(max_cols) <= 0)

    # hook length formula
    def dim_but_only_if_tabloid(self):
        if not self.is_tabloid():
            return "bruh read the method name"
        prod = 1
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                if self.values[row, col] != 0:
                    prod *= (np.count_nonzero(self.values[row, :]) - row) + \
                            (np.count_nonzero(self.values[:, col]) - col) - 1
        return int(math.factorial(np.count_nonzero(self.values)) / prod)

    def __eq__(self, other):
        return np.array_equal(self.values, other.values)

    def __hash__(self):
        total = 0
        for row in range(np.shape(self.values)[0]):
            for col in range(np.shape(self.values)[1]):
                total += (self.values[row, col] ** 3) ^ row ^ col
        return int(total)

    def __str__(self):
        return self.values.__str__()

    def __repr__(self):
        return self.values.__repr__()
