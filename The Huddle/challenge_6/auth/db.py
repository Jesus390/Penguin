from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Token(Base):
    """
    Tabla auxiliar para manejar tokens.
    """
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False)

    # Relaciones
    sesion_activa = relationship("SessionActiva", back_populates="token", cascade="all, delete-orphan")
    lista_negra = relationship("ListaNegra", back_populates="token", cascade="all, delete-orphan")

class SesionActiva(Base):
    """
    Control de sesiones activas
    
    Ejemplo: un usuario puede estar logueado en 2 dispositivos, guardás 
    sus tokens activos aquí.
    """
    __tablename__ = 'sesiones_activas'

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, ForeignKey('tokens.id', ondelete="CASCADE"), nullable=False)
    dispositivo = Column(String(100), nullable=False)

    # Relaciones
    token = relationship("Token", back_populates="sesion_activa", cascade="all, delete-orphan")

class ListaNegra(Base):
    """
    Lista negra (blacklist) de tokens
    
    Ejemplo: guardar tokens inválidos para rechazarlos después. 
    """
    __tablename__ = "listas_negras"

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(ForeignKey("tokens.id", ondelete="CASCADE"), nullable=False)
    motivo = Column(String(255), nullable=False)

    # Relaciones
    token = relationship("Token", back_populates="lista_negra", cascade="all, delete-orphan")


if __name__=="__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()
    ruta = os.getenv('PENGUIN_PATH')
    nombre_de_carpeta = "db/"
    nombre_de_archivo = "auth.db"

    # Crea la carpeta si no existe
    if not os.path.exists(ruta + nombre_de_carpeta):
        os.makedirs(ruta + nombre_de_carpeta)

    ruta_completa = ruta + nombre_de_carpeta + nombre_de_archivo

    engine = create_engine(f"sqlite:///{ruta_completa}")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()
