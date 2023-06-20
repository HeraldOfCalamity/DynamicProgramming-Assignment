class Etapa:
    def __init__(self, optimizacion=None, decision=None) -> None:
        self._optimizacion = optimizacion
        self._desicion = decision

    def get_optimizacion(self) -> dict:
        return self._optimizacion
    
    def get_decision(self) -> dict:
        return self._decision
    
    def set_optimizacion(self, optimizacion: dict) -> None:
        self._optimizacion = optimizacion

    def set_decision(self, decision: dict) -> None:
        self.get_decision = decision

    
