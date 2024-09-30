from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv

from db import SessionLocal, engine, Base, SQLALCHEMY_DATABASE_URL

# Carrega as variáveis do arquivo .env
load_dotenv()

app = FastAPI()

# Modelo para criação da tabela
class AlunoDB(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)


Base.metadata.create_all(bind=engine)


# Esquema Pydantic para validação de dados do aluno
class Aluno(BaseModel):
    id: int | None = None
    nome: str
    email: str

    class Config:
        from_attributes = True


# Dependencia para acessar o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Criação de um novo aluno
@app.post("/alunos/", response_model=Aluno)
def create_aluno(aluno: Aluno, db: Session = Depends(get_db)):
    db_aluno = AlunoDB(nome=aluno.nome, email=aluno.email)
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return Aluno.from_orm(db_aluno)

# Leitura de todos os alunos
@app.get("/alunos/", response_model=list[Aluno])
def read_alunos(db: Session = Depends(get_db)):
    return db.query(AlunoDB).all()

# Leitura de um aluno específico
@app.get("/alunos/{aluno_id}", response_model=Aluno)
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return Aluno.from_orm(aluno)

# Atualização de um aluno
@app.put("/alunos/{aluno_id}", response_model=Aluno)
def update_aluno(aluno_id: int, aluno_update: Aluno, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    aluno.nome = aluno_update.nome
    aluno.email = aluno_update.email
    db.commit()
    db.refresh(aluno)
    return Aluno.from_orm(aluno)

# Exclusão de um aluno
@app.delete("/alunos/{aluno_id}", response_model=Aluno)
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()
    return Aluno.from_orm(aluno)

