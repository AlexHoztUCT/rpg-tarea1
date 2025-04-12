# database.py

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Reemplaza 'user:password@localhost:3306/nombre_base_de_datos' con tus datos de conexión a MySQL
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/rpg "
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos de SQLAlchemy
class Personaje(Base):
    __tablename__ = "personajes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    xp = Column(Integer, default=0)
    misiones = relationship("PersonajeMision", back_populates="personaje")

class Mision(Base):
    __tablename__ = "misiones"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text)
    personajes = relationship("PersonajeMision", back_populates="mision")

class PersonajeMision(Base):
    __tablename__ = "personaje_mision"
    
    personaje_id = Column(Integer, ForeignKey('personajes.id'), primary_key=True)
    mision_id = Column(Integer, ForeignKey('misiones.id'), primary_key=True)
    
    personaje = relationship("Personaje", back_populates="misiones")
    mision = relationship("Mision", back_populates="personajes")

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)