from sqlalchemy import Column, DateTime, Boolean, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime, timezone

Base = declarative_base()

class Usuario(Base):
    """
    Información personal del usuario.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(100), nullable=False, unique=True)  # nombre de usuario único
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relaciones
    direcciones = relationship("Direccion", back_populates="usuario", cascade="all, delete-orphan")
    numeros_contacto = relationship("NumeroDeContacto", back_populates="usuario", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="usuario", cascade="all, delete-orphan")

class TipoDeContacto(Base):
    """
    Tipos de contacto del usuario.

    Ejemplo
    -------
    - Personal.
    - Laboral.
    - Etc.
    """
    __tablename__ = "tipos_de_contacto"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(100), nullable=False)
    descripcion = Column(String(255))

    # Relaciones
    direcciones = relationship("Direccion", back_populates="tipo_de_contacto", cascade="all, delete-orphan")
    numeros_contacto = relationship("NumeroDeContacto", back_populates="tipo_de_contacto", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="tipo_de_contacto", cascade="all, delete-orphan")


class Direccion(Base):
    """
    Contiene informaciones de las direcciones del usuario.
    """
    __tablename__ = "direcciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    direccion = Column(String(255), nullable=False)
    principal = Column(Boolean, default=False, nullable=False)
    tipo_de_contacto_id = Column(Integer, ForeignKey("tipos_de_contacto.id", ondelete="CASCADE"), nullable=False)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    

    # Relaciones
    usuario = relationship("Usuario", back_populates="direcciones")
    tipo_de_contacto = relationship("TipoDeContacto", back_populates="direcciones")

class NumeroDeContacto(Base):
    """
    Contiene informaciones de números telefonicos del usuario.
    """
    __tablename__ = "numeros_contactos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    telefono = Column(String(15), nullable=False, index=True)
    principal = Column(Boolean, default=False, nullable=False)
    tipo_de_contacto_id = Column(Integer, ForeignKey("tipos_de_contacto.id", ondelete="CASCADE"), nullable=False)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    

    usuario = relationship("Usuario", back_populates="numeros_contacto")
    tipo_de_contacto = relationship("TipoDeContacto", back_populates="numeros_contacto")

class Email(Base):
    """
    Contiene las direcciones de correo del usuario.
    """
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    principal = Column(Boolean, default=False, nullable=False)
    tipo_de_contacto_id = Column(Integer, ForeignKey("tipos_de_contacto.id", ondelete="CASCADE"), nullable=False)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    

    # Relaciones
    usuario = relationship("Usuario", back_populates="emails")
    tipo_de_contacto = relationship("TipoDeContacto", back_populates="emails")


if __name__=="__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()
    ruta = os.getenv('PENGUIN_PATH')
    nombre_de_carpeta = "challenge_6/db/"
    nombre_de_archivo = "users.db"

    # Crea la carpeta si no existe
    if not os.path.exists(ruta + nombre_de_carpeta):
        os.makedirs(ruta + nombre_de_carpeta)

    ruta_completa = ruta + nombre_de_carpeta + nombre_de_archivo

    engine = create_engine(f"sqlite:///{ruta_completa}")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()