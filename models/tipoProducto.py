from enum import Enum

class TipoProducto(Enum):
    PERECIBLE = 'PERECIBLE'
    NO_PERECIBLE = 'NO_PERECIBLE'
    OTRO = 'OTRO'   
    def serialize(self):
        return self.name

    @staticmethod
    def listar():
        return [producto.serialize() for producto in TipoProducto]