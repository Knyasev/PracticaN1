from models.producto import Producto
from app import db
import uuid
from models.persona import Persona
from models.rol import Rol
from datetime import datetime, timedelta,timezone
class ProductoController:
    def listar(self):
        return Producto.query.all()
    
    def listar_productos_buenos(self):
        return Producto.query.filter_by(estado="BUENO").all()
    
    
    def listar_productos_caducados(self):
        return Producto.query.filter_by(estado="CADUCADO").all()

    
    def modificar(self, data):
        producto = self.buscar_external(data.get("external_id"))
        if producto:
            producto.fecha_prod = data.get("fecha_prod")
            producto.fecha_venc = data.get("fecha_venc")
            producto.tipo_prdt = data.get("tipo_prdt")
            db.session.add(producto)
            db.session.commit()
            return producto.id
        else:
            return -1

    def buscar_external(self, external):
        return Producto.query.filter_by(external_id=external).first()    

   
    def desactivar(self,external_id):
        producto = self.buscar_external(external_id)
        if producto:
            producto.estado = "Caducado"
            db.session.commit()
            return producto.id
        else:
            return -1
        

    def registar_producto_persona(self, data):
        persona = Persona.query.filter_by(external_id=data.get("external_id")).first()
        if persona:
            producto = Producto()  # Crear una nueva instancia de Producto
            producto.external_id = data.get("producto_id")
            producto.nombre = data.get("nombre")
            producto.fecha_prod = data.get("fecha_prod")
            producto.fecha_venc = data.get("fecha_venc")
            producto.tipo_prdt = data.get("tipo_prdt")
            producto.estado = data.get("estado")
            persona.producto.append(producto)
            producto.stock =+1
            db.session.add(producto)
            db.session.commit() 
            return persona.id
        else:
            return -1
        

    def listarporCaducar(self):
            fecha_caducar = datetime.now(timezone.utc)+ timedelta(days=5)
            productos_por_caducar = Producto.query.filter(Producto.fecha_venc < fecha_caducar).all()
            for producto in productos_por_caducar:
                producto.estado = producto.estado.POR_CADUCAR  
                producto.stock =0
                db.session.commit()
            return productos_por_caducar
    
    def listarStock(self):
        Producto.query.filter_by(nombre="leche").all()
        total_stock = Producto.query.filter_by(stock=1).count()
        return total_stock
    