from sqlalchemy import Column, Integer, String, func
from src.models import Base, session 

class Clientes(Base):
    __tablename__ = 'Clientes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    direccion = Column(String(255), nullable=False)
    telefono = Column(String(20), unique=True, nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    activo = Column(Integer, default=True)

    @classmethod
    def get_by_cedula(cls, cedula):
        return session.query(cls).filter_by(cedula=cedula).first()
    
    def __init__(self, nombre, direccion, telefono, cedula, email, activo=True):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.cedula = cedula
        self.email = email
        self.activo = activo

    def save(self):
        session.add(self)
        session.commit()

    @staticmethod
    def get():
        clientes = session.query(Clientes).all()
        return clientes        
    
    @staticmethod
    def get_by_id(id):
        cliente = session.query(Clientes).filter_by(id=id).first()
        return cliente
    
    def update(self, nombre, direccion, telefono, cedula, email, activo):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.cedula = cedula
        self.email = email
        self.activo = activo
        session.commit()
    
    def delete(self):
        session.delete(self)
        session.commit()

    def to_dict(self):      
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "cedula": self.cedula,
            "email": self.email,
            "activo": self.activo
        }    
    def paginate(page=1, per_page=5):
        total = (session.query(func.count(Clientes.id)).scalar())
        clientes = session.query(Clientes).offset((page - 1) * per_page).limit(per_page).all()
        return clientes, total

