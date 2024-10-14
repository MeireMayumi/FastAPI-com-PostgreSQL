from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv
import os

from db import SessionLocal, engine, Base, SQLALCHEMY_DATABASE_URL

#Carrega as variáveis do arquivo .env
load_dotenv()

#Criação da instância da Aplicação FastAPI
app = FastAPI()

# Constante para o status "Aluno não encontrado"
ALUNO_NAO_ENCONTRADO = "Aluno não encontrado"

#Modelo que define a tabela alunos
class AlunoDB(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, autoincrement=True)  # id autoincrementado
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)

#Cria a tabela alunos no banco de dados, caso ela não exista
Base.metadata.create_all(bind=engine)


#Esquema Pydantic que define como os dados do aluno serão validados
class Aluno(BaseModel):
    id: int | None = None
    nome: str
    email: str
#Permite mapear dados do SQLAlchemy para este esquema
    class Config:
        from_attributes = True  


#Dependencia para acessar o banco de dados
def get_db():    # Função get_db() fornece uma sessão de banco de dados com SessionLocal, que foi definido no arquivo db.py
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()


#Criação de um novo aluno (id será gerado automaticamente)
@app.post("/alunos/", response_model=Aluno)
def create_aluno(aluno: Aluno, db: Session = Depends(get_db)):
    db_aluno = AlunoDB(nome=aluno.nome, email=aluno.email) 
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return Aluno.from_orm(db_aluno)

#Leitura de todos os alunos
@app.get("/alunos/", response_model=list[Aluno])
def read_alunos(db: Session = Depends(get_db)):
    return db.query(AlunoDB).all()

#Leitura de um aluno específico, baseado no id fornecido
@app.get("/alunos/{aluno_id}", response_model=Aluno)
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail=ALUNO_NAO_ENCONTRADO)
    return Aluno.from_orm(aluno)

#Atualização de informações um aluno exustente
@app.put("/alunos/{aluno_id}", response_model=Aluno)
def update_aluno(aluno_id: int, aluno_update: Aluno, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail=ALUNO_NAO_ENCONTRADO)
    aluno.nome = aluno_update.nome
    aluno.email = aluno_update.email
    db.commit()
    db.refresh(aluno)
    return Aluno.from_orm(aluno)

#Exclusão de um aluno baseado no id fornecido 
@app.delete("/alunos/{aluno_id}", response_model=Aluno)
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail=ALUNO_NAO_ENCONTRADO)
    db.delete(aluno)
    db.commit()
    return Aluno.from_orm(aluno)