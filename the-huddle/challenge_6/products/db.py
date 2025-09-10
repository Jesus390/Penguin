from sqlalchemy import Column, DateTime, Boolean, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime, timezone


Base = declarative_base()

class Categoria(Base):
    """
    Tipos de categorias para los productos.
    """
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=False, default="None")

    # Relaciones
    producto = relationship("Producto", back_populates="categorias", cascade="all, delete-orphan")


class Estado(Base):
    """
    Tipos de estados del producto (Pendiente, Vendido, Nulo, etc)
    """
    __tablename__ = "estados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=False, default="None")

    # Relaciones
    producto = relationship("Producto", back_populates="estados", cascade="all, delete-orphan")

class Producto(Base):
    """
    Información del producto.
    """
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    nombre = Column(String(100), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="CASCADE"), nullable=False)
    estado = Column(Integer, ForeignKey("estados.id", ondelete="CASCADE"), nullable=False)
    precio = Column(String(50), nullable=False)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relaciones
    categorias = relationship("Categoria", back_populates="producto")
    estados = relationship("Estado", back_populates="producto")

if __name__=="__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()
    ruta = os.getenv('PENGUIN_PATH')
    nombre_de_carpeta = "challenge_6/db/"
    nombre_de_archivo = "products.db"

    # Crea la carpeta si no existe
    if not os.path.exists(ruta + nombre_de_carpeta):
        os.makedirs(ruta + nombre_de_carpeta)

    ruta_completa = ruta + nombre_de_carpeta + nombre_de_archivo

    engine = create_engine(f"sqlite:///{ruta_completa}")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()
