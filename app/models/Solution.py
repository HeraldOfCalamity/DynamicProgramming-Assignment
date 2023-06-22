import copy
class Solution:

    def __init__(self):
        self.rangos = None
        self.d = None
        self.partialAnswer = {}
        self.answer = []

    def createDictonaryPartialAnswer(self):
        for index, (row, item) in enumerate(zip(self.rangos, self.d)):
            tdict = {}
            for i, j in zip(row, item):
                tdict[int(i)] = j
            self.partialAnswer[int(index)] = tdict

        return self.partialAnswer

    def showPr(self):
        return self.partialAnswer
    def create_answer(self):
        cpyPartialAnswer = copy.deepcopy(self.partialAnswer)
        etapa, dict = cpyPartialAnswer.popitem()
        clave, valor = dict.popitem()
        if isinstance(valor, int):
            valor = [valor]
        keysS = [clave - x for x in valor]
        partSol = [[x] for x in valor]
        for i in list(reversed(cpyPartialAnswer.keys())):
            keysS_copy = keysS.copy()
            for index, key in enumerate(keysS_copy):
                partSol[index].append(cpyPartialAnswer[i].get(key))
                keysS.append(key - cpyPartialAnswer[i].get(key))
                keysS.pop(0)
        print(partSol)
        return partSol

    def get_value_key(self, diccionario, valor):
        for clave, val in diccionario.items():
           if isinstance(val, list):
               if valor in val:
                   return clave
           else:
                if val == valor:
                    return clave
        return None
    def createSolutionMatrix(self):
        self.answer = []
        partsol = self.create_answer()
        for idx, item in enumerate(partsol):
            self.answer.append([])
            for x, pos in zip(item, range(-len(item)+1, 1)):
                row = [self.get_value_key(self.partialAnswer[pos*-1], x), x, self.get_value_key(self.partialAnswer[pos*-1], x)-x]
                self.answer[idx].append(row)

        return self.answer


