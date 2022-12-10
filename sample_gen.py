from itertools import permutations
from itertools import combinations
from itertools import product
from random import sample

import numpy as np
from Diagram import Diagram

# sign function again but for permutation
def sign(perm):
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return 1 - 2 * (inversions % 2)


size = 5
sample_size = 2
three_x_three = list(product(range(size), range(size)))
sort_by_dim = []
count = 1
for cells in sample(list(combinations(three_x_three, size)), sample_size):
    print(count)
    count += 1
    d = Diagram(cells)
    all_d_tabloids = set()
    for p in permutations([i + 1 for i in range(d.size)]):
        permuted = d.permute(p)
        all_d_tabloids.add(permuted)

    all_d_tabloids = list(all_d_tabloids)
    matrix = []
    for p in permutations([i + 1 for i in range(d.size)]):
        poly_tab = d.polytabloid()
        new_poly_tab = set()
        for tab in poly_tab:
            permuted = tab.permute(p)
            one_line_perm = permuted.values[np.nonzero(permuted.values)].tolist()
            new_poly_tab.add((permuted, sign(one_line_perm)))
        vec = []
        for i in range(len(all_d_tabloids)):
            if (all_d_tabloids[i], 1) in new_poly_tab:
                vec.append(sign(p))
            elif (all_d_tabloids[i], -1) in new_poly_tab:
                vec.append(-sign(p))
            else:
                vec.append(0)
        matrix.append(vec)
    matrix = np.asmatrix(matrix)
    rank = np.linalg.matrix_rank(matrix)
    sort_by_dim.append((rank, d))

sort_by_dim = sorted(sort_by_dim, key=lambda x: x[0])
seen = set()
for (rank, d) in sort_by_dim:
    d.latex(size, size)
    print("\\quad dim =", rank, " \\vspace{0.4cm}")
    print("\\hrule\\vspace{0.3cm}")
    print()
    print()
    seen.add(rank)
print(sorted(seen))
