from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Float, func

from src.models import Base, session


class Facturas(Base):
    __tablename__ = 'Facturas'

    id = Column(Integer, primary_key=True)
    numero_factura = Column(
        String(50),
        unique=True,
        nullable=False
    )
    fecha_emision = Column(String(50), nullable=False)
    Cliente_id = Column(
        Integer,
        ForeignKey('Clientes.id'),
        nullable=False
    )
    Vendedor_id = Column(
        Integer,
        ForeignKey('Vendedores.id'),
        nullable=False
    )

    def __init__(
        self,
        numero_factura,
        fecha_emision,
        cliente_id,
        vendedor_id
    ):
        self.numero_factura = numero_factura
        self.fecha_emision = fecha_emision
        self.Cliente_id = cliente_id
        self.Vendedor_id = vendedor_id

    def save(self):
        session.add(self)
        session.commit()

    def get():
        return session.query(Facturas).all()

    @staticmethod
    def get_by_id(id):
        return session.query(Facturas).filter_by(id=id).first()

    def delete(self):
        session.delete(self)
        session.commit()

    def total_factura(self):
        from src.models.Detalle_facturas import Detalle_Facturas

        total = session.query(
            func.coalesce(
                func.sum(Detalle_Facturas.total),
                0
            )
        ).filter(
            Detalle_Facturas.factura_id == self.id
        ).scalar()

        return float(total)

    def productos_factura(self):
        from src.models.Detalle_facturas import Detalle_Facturas
        from src.models.Productos import Productos

        detalles = session.query(
            Detalle_Facturas,
            Productos
        ).join(
            Productos,
            Productos.id == Detalle_Facturas.producto_id
        ).filter(
            Detalle_Facturas.factura_id == self.id
        ).all()

        return [
            {
                "id": producto.id,
                "nombre": producto.nombre,
                "cantidad": detalle.cantidad,
                "precio_unitario": float(
                    detalle.precio_unitario
                ),
                "total": float(detalle.total)
            }
            for detalle, producto in detalles
        ]

    def to_dict(self):
        return {
            "id": self.id,
            "numero_factura": self.numero_factura,
            "fecha_emision": self.fecha_emision,
            "cliente_id": self.Cliente_id,
            "vendedor_id": self.Vendedor_id,
            "productos": self.productos_factura(),
            "total": self.total_factura()
        }

    @staticmethod
    def paginate(page=1, per_page=5):
        total = session.query(
            func.count(Facturas.id)
        ).scalar()

        facturas = session.query(Facturas).offset(
            (page - 1) * per_page
        ).limit(per_page).all()

        return facturas, total