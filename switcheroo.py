import numpy as np
from Diagrameaux import Diagrameaux


# ignore TODO
def remove_stragglers(diagram):
    num_rows, num_cols = np.shape(diagram.values)
    row = 0
    while row < num_rows:
        if not np.any(diagram.values[row, :]):
            values = np.delete(values, row, axis=0)
            num_rows -= 1
        else:
            row += 1

    col = 0
    while col < num_cols:
        if not np.any(diagram.values[:, col]):
            values = np.delete(values, col, axis=1)
            num_cols -= 1
        else:
            col += 1

def diagram_to_tabloids(diagram, seen=None):
    if seen is None:
        seen = set()
    if diagram.is_tabloid() and diagram not in seen:
        print(diagram.values)
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
    print(diagram.values, valid_moves)
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


# boxes = Diagram([(0, 0), (0, 1), (0, 3), (1, 3), (2, 3)]).values
# ^ for if you want to type box coordinates instead
boxes = [[0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0],
         [0, 0, 0, 1, 1],
         [1, 0, 0, 0, 0]]
d = Diagrameaux(boxes)
print(d.values)
print(diagram_to_tabloids(d))
