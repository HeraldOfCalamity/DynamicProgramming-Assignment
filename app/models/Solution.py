import numpy as np
class Solution:

    def __init__(self):
        self.rangos = None
        self.d = None
        self.partialAnswer = {}

    def createDictonaryPartialAnswer(self):
        for index, (row, item) in enumerate(zip(self.rangos, self.d)):
            tdict = {}
            for i, j in zip(row, item):
                tdict[int(i)] = j
            self.partialAnswer[int(index)] = tdict
        return self.partialAnswer


    def create_answer(self):
        respuesta = np.zeros((len(self.partialAnswer), 4))
        for index, i in enumerate(range(-len(self.partialAnswer)+1, 1)):
            respuesta