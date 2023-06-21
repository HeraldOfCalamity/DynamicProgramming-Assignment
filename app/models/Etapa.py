import numpy as np


class Etapa:
    def __init__(self) -> None:
        self.rows = 0
        self.columns = 0
        self.matrix = np.matrix

    def set_Size_of_Matrix(self, rows, columns):
        """
        :param rows: is an array/tuple
        :param columns: array
        :return: a matrix of zeros
        """

        self.rows = rows
        self.columns = columns
        self.matrix = np.zeros([rows, columns])
        return self.matrix

    # return self.matrix[:, objetive].tolist()

    def process(self, r, f):
        for fila in range(self.rows):
            for col, i in zip(range(self.columns), range(len(f))):
                if col <= fila:
                    if col > 0:
                        self.matrix[fila, col] = r[col][0] + f[fila-i]
                    else:
                        self.matrix[fila, col] = r[col][0] + f[fila]


    def last_iteration(self, r, f):
        for fila in range(self.rows):
            for col, i in zip(range(self.columns), range(1, len(f)+1)):
                self.matrix[fila, col] = r[col][0] + f[-i]

    def maxOrMin(self, case='Max'):
        if case.lower() == 'max':
            return np.amax(self.matrix, axis=1)
        else:
            return np.ma.masked_equal(self.matrix, 0).min(axis=1)

    def iterations(self, r, f, li):
        if li:
            self.last_iteration(r, f)
        else:
            self.process(r, f)
        print(self.matrix)
        return self.maxOrMin("max")
