from sqlalchemy import Column, Integer, String, func
from src.models import Base, session

class Vendedores(Base):
    __tablename__ = 'Vendedores'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telefono = Column(String(20), unique=True, nullable=False)
    direccion = Column(String(255), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    activo = Column(Integer, default=True)

    def __init__(self, nombre, email, telefono, direccion, cedula, activo=True):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.cedula = cedula
        self.activo = activo

    def save(self):
        session.add(self)
        session.commit()

    def get():
        vendedores = session.query(Vendedores).all()
        return vendedores
    
    @staticmethod
    def get_by_id(id):
        vendedor = session.query(Vendedores).filter_by(id=id).first()
        return vendedor

    def delete(self):
        session.delete(self)
        session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "cedula": self.cedula,
            "activo": self.activo
        }   

    def paginate(page=1, per_page=5):
        total = (session.query(func.count(Vendedores.id)).scalar())
        vendedores = session.query(Vendedores).offset((page - 1) * per_page).limit(per_page).all()
        return vendedores, total

    