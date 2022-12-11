import numpy as np
from Diagrameaux import Diagrameaux


def stragglers_removed(diagram):
    destraggled = np.copy(diagram.values)
    straggle_count = 0
    num_rows, num_cols = np.shape(destraggled)
    for row in range(num_rows):
        for col in range(num_cols):
            if np.sum(destraggled[row, :]) + np.sum(destraggled[:, col]) \
                    - 2 * destraggled[row][col] == 0:
                destraggled[row][col] = 0
                straggle_count += 1
    return Diagrameaux(destraggled), straggle_count


def diagram_to_tabloids(diagram, seen=None):
    if seen is None:
        seen = set()
    if diagram.is_tabloid() and diagram not in seen:
        print(diagram.dim_but_only_if_tabloid())
        return diagram.dim_but_only_if_tabloid(), {diagram}
    if diagram.is_tabloid():
        return 0, {diagram}
    valid_moves = [[], []]
    for row in range(diagram.num_rows()):
        if row != 0 and not set(np.nonzero(diagram.values[row, :])[0].flatten()) \
                .issubset(set(np.nonzero(diagram.values[row - 1, :])[0].flatten())):
            valid_moves[0].append(row)
    for col in range(diagram.num_cols()):
        if col != 0 and not set(np.nonzero(diagram.values[:, col])[0].flatten()) \
                .issubset(set(np.nonzero(diagram.values[:, col - 1])[0].flatten())):
            valid_moves[1].append(col)
    total = 0
    for row in valid_moves[0]:
        dim, tab = diagram_to_tabloids(diagram.row_up(row), seen)
        total += dim
        seen = seen.union(tab)
    for col in valid_moves[1]:
        dim, tab = diagram_to_tabloids(diagram.col_left(col), seen)
        total += dim
        seen = seen.union(tab)
    return total, seen

# multiplier for straggler with n boxes total, k stragglers
def straggler_factor(n, k):
    prod = 1
    for i in range(k):
        prod *= n - i
    return prod


# boxes = Diagram([(0, 0), (0, 1), (0, 3), (1, 3), (2, 3)]).values
# ^ for if you want to type box coordinates instead
boxes = [[1, 1, 1, 0, 0, 0],
         [1, 0, 1, 0, 0, 0],
         [1, 1, 1, 1, 0, 0],
         [0, 0, 1, 1, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]
'''boxes = [[1, 0, 1],
         [0, 0, 0]]'''
n = np.count_nonzero(boxes)
d = Diagrameaux(boxes)
print(d)
d, k = stragglers_removed(d)
dim, reached = diagram_to_tabloids(d)
print(dim * straggler_factor(n, k))
print(reached)
