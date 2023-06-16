class Asignacion:
    def __init__(self, destinos=None, opciones=None, caso='MAX') -> None:
        self._destinos = destinos
        self._opciones = opciones
        self._caso = caso
    
    def get_destinos(self) -> list:
        return self._destinos
    
    def get_opciones(self) -> list:
        return self._opciones
    
    def set_destinos(self, destinos) -> None:
        self._destinos = destinos

    def set_opciones(self, opciones) -> None:
        self._opciones = opciones

    def get_caso(self) -> str:
        return self._caso
    
    def set_caso(self, caso: str) -> None:
        self._caso = caso

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
    
