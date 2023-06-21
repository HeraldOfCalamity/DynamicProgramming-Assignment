import numpy as np
class Matrix:
    def __init__(self) -> None:
        self.rows = 0
        self.columns = 0
        self.matrix = np.matrix

    def set_Size_of_Matrix(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = np.zeros([rows, columns])
        return self.matrix

    def fill_Matrix(self, matrix):
        self.matrix = np.matrix(matrix)

    def getBenefits(self, objetive) -> list:
        return self.matrix[:, objetive].tolist()