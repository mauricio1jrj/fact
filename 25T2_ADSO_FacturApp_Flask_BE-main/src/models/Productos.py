from sqlalchemy import Column, Integer, String, Float, ForeignKey, func
from src.models import Base, session

class Productos(Base):
    __tablename__ = 'Productos'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=False)
    unidad_medida = Column(String(50), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    Categoria_id = Column(Integer, ForeignKey('Categorias.id'), nullable=False)


    def __init__(self, codigo, nombre, descripcion, unidad_medida, precio, stock, categoria_id):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.unidad_medida = unidad_medida
        self.precio = precio
        self.stock = stock
        self.Categoria_id = categoria_id

    def save(self):
        session.add(self)
        session.commit()

    def get():
        productos = session.query(Productos).all()
        return productos
    
    @staticmethod
    def get_by_id(id):
        producto = session.query(Productos).filter_by(id=id).first()
        return producto

    def delete(self):
        session.delete(self)
        session.commit()

    #to_dict() serializa los atributos de un objeto en un diccionario de Python, permitiendo que jsonify() de Flask los transforme en formato JSON.
    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "unidad_medida": self.unidad_medida,
            "precio": self.precio,
            "stock": self.stock,
            "categoria_id": self.Categoria_id
        }
    def paginate(page=1, per_page=5):
        total = (session.query(func.count(Productos.id)).scalar())
        productos = session.query(Productos).offset((page - 1) * per_page).limit(per_page).all()
        return productos, total
       
