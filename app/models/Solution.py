import numpy as np
class Solution:

    def __init__(self):
        self.rangos = None
        self.d = None
        self.partialAnswer = {}
        self.answer = np.matrix

    def createDictonaryPartialAnswer(self):
        for index, (row, item) in enumerate(zip(self.rangos, self.d)):
            tdict = {}
            for i, j in zip(row, item):
                tdict[int(i)] = j
            self.partialAnswer[int(index)] = tdict

        self.answer = np.zeros((len(self.partialAnswer), 4))
        return self.partialAnswer


    def create_answer(self, dest):
        # for i, row in enumerate(self.answer):
        #     row[0] = dest[i].get_nombre()
        for key in reversed(self.partialAnswer.keys()):
            print(key)



