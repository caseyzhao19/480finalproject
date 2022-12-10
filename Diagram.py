import sys
import copy
from itertools import permutations
from itertools import product
from operator import itemgetter
import numpy as np

np.set_printoptions(threshold=sys.maxsize)

# NO MOD OR U WILL BE SAD :'(, treat basically as read-only
class Diagram:
    def __init__(self, entries):
        self.entries = sorted(entries)
        self.size = len(self.entries)
        self.num_rows = max(self.entries, key=itemgetter(0))[0] + 1
        self.num_cols = max(self.entries, key=itemgetter(1))[1] + 1
        self.values = np.zeros((self.num_rows, self.num_cols), int)

        for k in range(self.size):
            (i, j) = self.entries[k]
            self.values[i][j] = k + 1

        self.row_stabilizer = []
        for row_idx in range(self.num_rows):
            row = self.values[row_idx, :]
            self.row_stabilizer.append(row[np.nonzero(row)].tolist())

        self.col_stabilizer = []
        for col_idx in range(self.num_cols):
            col = self.values[:, col_idx]
            self.col_stabilizer.append(col[np.nonzero(col)].tolist())

    def __copy__(self, same_dim=False):
        if same_dim:
            return Diagram(self.entries.copy())
        return Diagram(self.entries.copy())

    def permute(self, pi):
        permed = copy.copy(self)
        for i in range(len(pi)):
            permed.values[self.values == i + 1] = pi[i]
        return permed

    def latex(self, r=-1, c=-1):
        print("\\begin{ytableau}")
        num_rows = self.num_rows
        num_cols = self.num_cols
        if r != -1 and c != -1:
            num_rows = r
            num_cols = c
        for row in range(num_rows):
            print("\t ", end="")
            replace_zeroes = [self.values[row, col] if col < self.num_cols and row < self.num_rows
                              else 0 for col in range(num_cols)]
            for idx in range(len(replace_zeroes)):
                if replace_zeroes[idx] == 0:
                    replace_zeroes[idx] = "\\none"
            print(*replace_zeroes, sep=" & ", end=" ")
            if row != num_rows - 1:
                print("\\\\")
        print("\n\\end{ytableau}")

    def polytabloid(self):
        perms = []
        for subgroup in self.col_stabilizer:
            sub_perms = []
            for p in permutations(subgroup):
                array_form = [0 for i in range(self.size)]
                for i in range(len(subgroup)):
                    idx = subgroup[i] - 1
                    array_form[idx] = p[i]
                sub_perms.append(array_form)
            perms.append(sub_perms)
        prod = product(*perms)
        perms = []
        for i in prod:
            perms.append([sum(j) for j in zip(*i)])
        perms = sorted(perms)

        set_of_tabloids = set()
        for perm in perms:
            set_of_tabloids.add(self.permute(perm))
        # for tab in set_of_tabloids:
        #    tab.latex()
        return set_of_tabloids

    def __eq__(self, other):
        if self.num_rows != other.num_rows:
            return False
        for row in range(self.num_rows):
            if set(self.values[row, :]) != set(other.values[row, :]):
                return False
        return True

    def __hash__(self):
        return int(sum([sum(self.values[row, :]) * (row + 1) ** 3 for row in range(self.num_rows)]))

    def sign(self):
        perm = self.values[np.nonzero(self.values)].tolist()
        inversions = 0
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if perm[i] > perm[j]:
                    inversions += 1
        return 1 - 2 * (inversions % 2)



