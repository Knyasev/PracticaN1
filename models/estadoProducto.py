from enum import Enum

class EstadoProducto(Enum):
    BUENO = 'BUENO'
    CADUCADO = 'CADUCADO'
    POR_CADUCAR = 'POR_CADUCAR'
    @property
    def serialize(self):
        return {
            'name': self.name
        }
    @staticmethod
    def listar ():
        return [e.value for e in EstadoProducto]