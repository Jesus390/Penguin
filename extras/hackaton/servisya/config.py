import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-segura'
    
    # Base de datos SQLite ubicada en la carpeta 'instance'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///serviya.db'
    
    # Desactiva una advertencia innecesaria
    SQLALCHEMY_TRACK_MODIFICATIONS = False
