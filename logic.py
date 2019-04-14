import random

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


def matching(binary_matrix, size):
    # найдем сначала координаты точек, которые уже образуют 3 в ряд по y или x
    global s
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
    print(s_array)
    for i in range(size[0]):
        optional_elems(s_array[i], binary_matrix, size)
    return s


arr = [[0, 0, 0, 0, 0, 0],
       [0, 1, 1, 1, 1, 0],
       [0, 1, 1, 0, 0, 0],
       [0, 0, 1, 1, 0, 0],
       [1, 0, 1, 0, 1, 0],
       [1, 0, 1, 1, 0, 0]]
print(sorted(list(matching(arr, (6, 6)))))


# тут будет на выходе матрица из нулей и единичек
def to_binary_matrix(matrix, size, name):
    pass


class Area:
    def __init__(self, size):
        self.size = size

    def matrix(self):
        pass
