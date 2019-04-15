import random
from pprint import pprint
import copy

# диагонали игнорируются
# size - (y, x)

s = set()


def optional_elems(coords, binary_matrix, size):
    global s
    y, x = coords
    delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for k in delta:
        dy, dx = k
        if y + dy not in range(size[0]):
            continue
        if x + dx not in range(size[1]):
            continue
        if binary_matrix[y + dy][x + dx] == 0:
            continue
        if (y + dy, x + dx) not in s:
            s.add((y + dy, x + dx))
            optional_elems((y + dy, x + dx), binary_matrix, size)


def matching(binary_matrix, size, check=False):
    # найдем сначала координаты точек, которые уже образуют 3 в ряд по y или x
    global s
    s.clear()
    for i in range(size[0]):
        for k in range(size[1]):
            if binary_matrix[i][k] == 0:
                continue
            if k + 3 <= size[1]:
                if binary_matrix[i][k] == binary_matrix[i][k + 1] == binary_matrix[i][k + 2]:
                    for j in range(3):
                        s.add((i, k + j))
            if i + 3 <= size[0]:
                if binary_matrix[i][k] == binary_matrix[i + 1][k] == binary_matrix[i + 2][k]:
                    for j in range(3):
                        s.add((i + j, k))
    s_array = sorted(list(s))
    if check:
        return bool(s_array)
    # print(s_array)
    for i in range(size[0]):
        optional_elems(s_array[i], binary_matrix, size)
    return s


# тут будет на выходе матрица из нулей и единичек
def to_binary_matrix(matrix, size, index):
    binary_matrix = [matrix[i] for i in range(size[0])]
    for i in range(size[0]):
        for j in range(size[1]):
            if binary_matrix[i][j] == index:
                binary_matrix[i][j] = 1
            else:
                binary_matrix[i][j] = 0
    return binary_matrix


# N - кол-во уникальных элементов (картиночек)
N = 5

elements = {1: '', 2: '', 3: ''}


class Area:
    def __init__(self, size):
        self.size = size
        self.zero = 0
        self.arr = [[0] * size[1] for x in range(size[0])]

    def matrix(self):
        conseq = [True for x in range(N)]
        while True in conseq:
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    r = random.randint(1, N)  # границы включительно
                    self.arr[i][j] = r
            for i in range(N):
                conseq[i] = matching(to_binary_matrix(copy.deepcopy(self.arr), self.size, i + 1), self.size, check=True)


a = Area((13, 13))
a.matrix()
pprint(a.arr)
