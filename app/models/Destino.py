class Destino:
    def __init__(self, nombre=None, benefit=None, rango=None) -> None:
        self._nombre = str(nombre)
        self._benefit = benefit
        self._rango = rango

    def __str__(self) -> str:
        return f'Nombre: {self._nombre}, Beneficios: {self._benefit}'

    def get_nombre(self) -> str:
        return self._nombre
    
    def get_benefit(self) -> dict:
        return self._benefit
    
    def get_rango(self) -> tuple|int:
        return self._rango

    def get_min_asig(self) -> int:
        try:
            return min(self._benefit)
        except:
            print('Error en llaves')

    def set_benefit(self, benefit: dict):
        self._benefit = benefit

    def set_nombre(self, nombre: str)-> None:
        self._nombre = nombre

    def set_rango(self, rango: tuple|int) -> None:
        self._rango = rango

    

        