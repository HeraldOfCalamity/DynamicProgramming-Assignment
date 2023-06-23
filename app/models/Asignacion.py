class Asignacion:
    def __init__(self, destinos=None, opciones=None, caso='MAX', recurso: int=None) -> None:
        self._destinos = destinos
        self._opciones = opciones
        self._caso = caso
        self._recurso = recurso
        self._solucion = None
        self._etapas = []
        self._rangos = None
        self._fs = []
        self._ds = []

    def __str__(self) -> str:
        return str(self._destinos) + '\n' + str(self._opciones)

    def get_destinos(self) -> list:
        return self._destinos
    
    def get_opciones(self) -> list:
        return self._opciones
    
    def get_caso(self) -> str:
        return self._caso
    
    def get_recurso(self) -> int:
        return self._recurso

    def set_destinos(self, destinos) -> None:
        self._destinos = destinos

    def set_opciones(self, opciones) -> None:
        self._opciones = opciones

    def set_caso(self, caso: str) -> None:
        self._caso = caso

    def set_recurso(self, recurso: int) -> None:
        self._recurso = recurso

    def get_funcion_objetivo(self) -> str:
        n = len(self._destinos)
        d = ''
        rxd = '{'
        for i in range(n, 0, -1):
            rxd += f'r_{i}(x_{i}, d_{i}) + ' if i > 1 else f'r_{i}(x_{i}, d_{i})' + '}' 
            d += f'd_{i}, ' if i > 1 else f'd_{i} '

        return f'f_{n}*(x_{n}) = {self._caso} ' + d + rxd
    
    def get_eficiencia(self) -> str:
        return 'x_(k-1) = x_k - d_k'

    def get_transicion(self) -> str:
        n = len(self._destinos)
        return f'f_k*(x_k) = {self._caso} d_k' + '{ r_k(x_k, d_k) + f_k-1(x_k-1) }'
    
    def _leftSum(self):
        left = 0
        for dest in self._destinos:
            left += dest.get_min_asig()
        return left

    def set_rangos(self, rangos):
        self._rangos = rangos

    def get_rangos(self):
        right = 0
        left = self._leftSum()

        for dest in reversed(self._destinos):
            minAsig = dest.get_min_asig()
            right += minAsig    
            left -= minAsig
            dest.set_rango((right, self._recurso - left))
        return self._rangos

    def get_matriz(self):
        mtx = []
        i = 0
        for op in self._opciones:
            mtx.append([])
            for dest in self.get_destinos():
                mtx[i].append(dest.get_benefit()[op])
            i += 1
        return mtx

    def get_solution(self):
        return self._solucion

    def set_solution(self, sol):
        self._solucion = sol


    def set_etapas(self,etapas):
        self._etapas = etapas

    def get_etapas(self):
        return self._etapas

    def get_fs(self):
        return self._fs

    def set_fs(self, fs):
        self._fs = fs

    def get_ds(self):
        return self._ds

    def get_formated_ds(self):
        return self.reformat(self._ds)
    def set_ds(self, ds):
        self._ds = self.reformat(ds)

    def reformat(self, alist):
        nlist = []
        for row in alist:
            tlist = []
            for i in row:
                if len(i) > 1:
                    tlist.append(i)
                else:
                    tlist.append(i[0])
            nlist.append(tlist)
        return nlist

