from models.producto import Producto
from app import db
import uuid
from models.persona import Persona
from models.rol import Rol
from datetime import datetime, timedelta,timezone
from models.lote import Lote    
class ProductoController:
    def listar(self):
        return Producto.query.all()
    
    def listar_productos_buenos(self):
        return Producto.query.filter_by(estado="BUENO").all()
        
    def listar_productos_caducados(self):
        return Producto.query.filter_by(estado="CADUCADO").all()
    
    def listar_productos_por_caducar(self):
        return Producto.query.filter_by(estado="POR_CADUCAR").all()

    
    def modificar(self, data):
        producto = self.buscar_external(data.get("external_id"))
        if producto:
            producto.nombre = data.get("nombre")
            producto.fecha_prod = data.get("fecha_prod")
            producto.fecha_venc = data.get("fecha_venc")
            producto.estado = data.get("estado")
            producto.precio = data.get("precio")
            producto.status = data.get("status")
            db.session.commit()
            return producto.id

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
        lote = Lote.query.filter_by(external_id=data.get("extenal_id_lote")).first()
        if lote:
            productos_existentes = Producto.query.filter_by(lote_id=lote.id).count()
            if productos_existentes >= lote.cantidad:
                return -2  
            producto = Producto()  
            producto.external_id = str(uuid.uuid4())
            producto.nombre = lote.nombre
            producto.fecha_prod = data.get("fecha_prod")
            producto.fecha_venc = data.get("fecha_venc")
            producto.estado = data.get("estado")
            producto.lote_id= lote.id
            producto.precio = data.get("precio")
            producto.status = True
            producto.stock = lote.cantidad  # Establecer el stock al valor de la cantidad del lote
            db.session.add(producto)
            db.session.commit() 
            return producto
        else:
            return -1


    def listarporCaducar(self):
        fecha_caducar = datetime.now(timezone.utc) + timedelta(days=5)
        lotes = Lote.query.all()
        productos_por_caducar_por_lote = {}
    
        for lote in lotes:
            productos_por_caducar = Producto.query.filter(Producto.fecha_venc <= fecha_caducar, Producto.lote_id == lote.id).all()
            productos_por_caducar_por_lote[lote.nombre] = productos_por_caducar
    
            for producto in productos_por_caducar:
                if producto.status == True:
                    producto.estado = producto.estado.POR_CADUCAR 
                    producto.status = False
                    producto.stock -= len(productos_por_caducar) 
                else:
                    producto.estado = producto.estado.POR_CADUCAR
            db.session.commit()
        return productos_por_caducar_por_lote
    
    def listarCaducados(self):
        fecha_actual = datetime.now(timezone.utc)
        lotes = Lote.query.all()
        productos_caducados_por_lote = {}
    
        for lote in lotes:
            productos_caducados = Producto.query.filter(Producto.fecha_venc < fecha_actual, Producto.lote_id == lote.id).all()
            productos_caducados_por_lote[lote.nombre] = productos_caducados
            for producto in productos_caducados:
                if producto.status == True:
                    producto.estado = producto.estado.CADUCADO
                    producto.status = False
                    producto.stock -= len(productos_caducados) # Reduce el stock del producto en 1
                else:
                    producto.estado = producto.estado.CADUCADO
        db.session.commit()
    
        return productos_caducados_por_lote
    
    