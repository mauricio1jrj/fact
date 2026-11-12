from sqlalchemy import Column, Integer, String, func
from src.models import Base, session 

class Categorias(Base):
    __tablename__ = 'Categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def save(self):
        session.add(self)
        session.commit()

    @staticmethod
    def get():
        categorias = session.query(Categorias).all()
        return categorias

    @staticmethod
    def get_by_id(id):
        categoria = session.query(Categorias).filter_by(id=id).first()
        return categoria

    @staticmethod
    def create(nombre):
        categoria = Categorias(nombre=nombre)
        session.add(categoria)
        session.commit()
        return categoria

    @staticmethod
    def update(id, nombre):
        categoria = Categorias.get_by_id(id)
        if categoria:
            categoria.nombre = nombre
            session.commit()
        return categoria

    @staticmethod
    def delete(id):
        categoria = Categorias.get_by_id(id)
        if categoria:
            session.delete(categoria)
            session.commit()
        return categoria

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }    
    def paginate(page=1, per_page=5):
        total = (session.query(func.count(Categorias.id)).scalar())
        categorias = session.query(Categorias).offset((page - 1) * per_page).limit(per_page).all()
        return categorias, total
    