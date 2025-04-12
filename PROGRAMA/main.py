# main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, List
from database import SessionLocal, Personaje, Mision, PersonajeMision
from Cola import Cola
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos Pydantic
class PersonajeCreate(BaseModel):
    id: int
    nombre: str

class MisionCreate(BaseModel):
    id: int
    descripcion: str

# Utilidades de sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicialización de las colas
colas_misiones: Dict[int, Cola] = {}

# Rutas de la API
@app.post("/personajes", response_model=Personaje)
def crear_personaje(personaje: PersonajeCreate, db: Session = Depends(get_db)):
    db_personaje = Personaje(**personaje.dict())
    db.add(db_personaje)
    db.commit()
    db.refresh(db_personaje)
    colas_misiones[personaje.id] = Cola()  # Inicializa cola para el personaje
    return db_personaje

@app.post("/misiones", response_model=Mision)
def crear_mision(mision: MisionCreate, db: Session = Depends(get_db)):
    db_mision = Mision(**mision.dict())
    db.add(db_mision)
    db.commit()
    db.refresh(db_mision)
    return db_mision

@app.post("/personajes/{id}/misiones/{mision_id}")
def aceptar_mision(id: int, mision_id: int, db: Session = Depends(get_db)):
    db_personaje = db.query(Personaje).filter(Personaje.id == id).first()
    if not db_personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    
    db_mision = db.query(Mision).filter(Mision.id == mision_id).first()
    if not db_mision:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    
    # Encolar la misión
    if id not in colas_misiones:
        colas_misiones[id] = Cola()
    
    colas_misiones[id].enqueue(db_mision)
    return {"mensaje": "Misión aceptada", "mision": db_mision.descripcion}

@app.post("/personajes/{id}/completar")
def completar_mision(id: int, db: Session = Depends(get_db)):
    db_personaje = db.query(Personaje).filter(Personaje.id == id).first()
    if not db_personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    cola = colas_misiones.get(id)
    if cola is None or cola.is_empty():
        raise HTTPException(status_code=404, detail="No hay misiones en la cola")

    mision_completada = cola.dequeue()
    db_personaje.xp += 10  # Sumar experiencia (ejemplo)
    
    return {"mensaje": "Misión completada", "mision": mision_completada.descripcion, "xp_actual": db_personaje.xp}

@app.get("/personajes/{id}/misiones", response_model=List[Mision])
def listar_misiones(id: int, db: Session = Depends(get_db)):
    db_personaje = db.query(Personaje).filter(Personaje.id == id).first()
    if not db_personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    if id not in colas_misiones:
        return []

    return colas_misiones[id].items