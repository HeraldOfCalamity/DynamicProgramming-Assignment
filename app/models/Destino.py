class Destino:
    def __init__(self, nombre, benefit) -> None:
        self._nombre = str(nombre)
        self._benefit = benefit

    def __str__(self) -> str:
        return f'Nombre: {self._nombre}, Beneficios: {self._benefit}'

    def get_nombre(self) -> str:
        return self._nombre
    
    def get_benefit(self) -> str:
        return self._benefit
    
    def get_min_asig(self) -> int:
        pass


        