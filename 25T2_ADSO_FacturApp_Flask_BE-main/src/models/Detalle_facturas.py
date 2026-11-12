from sqlalchemy import Column, Integer, Float, ForeignKey, func
from src.models.Vendedores import Vendedores
from src.models import Base, session

class Detalle_Facturas(Base):
    __tablename__ = 'Detalle_Facturas'

    id = Column(Integer, primary_key=True)
    factura_id = Column(Integer, ForeignKey('Facturas.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('Productos.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    def __init__(self, factura_id, producto_id, cantidad, precio_unitario, total):
        self.factura_id = factura_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total = total

    def save(self):
        session.add(self)
        session.commit()

    def get():
        detalle_facturas = session.query(Detalle_Facturas).all()
        return detalle_facturas
    
    @staticmethod
    def get_by_id(id):
        detalle_factura = session.query(Detalle_Facturas).filter_by(id=id).first()
        return detalle_factura

    def delete(self):
        session.delete(self)
        session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "factura_id": self.factura_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "total": self.total
        }
    def paginate(page=1, per_page=5):
        total = (session.query(func.count(Detalle_Facturas.id)).scalar())
        detalle_facturas = session.query(Detalle_Facturas).offset((page - 1) * per_page).limit(per_page).all()
        return detalle_facturas, total 