import numpy as np


class Etapa:
    def __init__(self) -> None:
        self.rows = 0
        self.columns = 0
        self.matrix = np.matrix
    def set_Size_of_Matrix(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = np.zeros([rows, columns])
        return self.matrix

    # return self.matrix[:, objetive].tolist()

    def process(self, r, f):
        for fila in range(self.rows):
            for col in range(self.columns):
                if col <= fila:
                    self.matrix[fila, col] = r[col][0] + f[col]

    def maxOrMin(self, case='Max'):
        if case.lower() == 'max':
            return np.amax(self.matrix, axis=1)
        else:
            return np.ma.masked_equal(self.matrix, 0).min(axis=1)

    def iterations(self, r, f):
        self.process(r, f)
        print(self.matrix)
        f = self.maxOrMin("min")



