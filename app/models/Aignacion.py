class Asignacion:
    def __init__(self, destinos, opciones) -> None:
        self._destinos = destinos
        self._opciones = opciones
        
    
    def get_destinos(self) -> list:
        return self._destinos
    
    def get_opciones(self) -> list:
        return self._opciones