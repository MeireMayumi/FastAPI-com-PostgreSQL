# FastAPI com PostgreSQL

Esta API permite a execução das quatro operações básicas **CRUD** (Create, Read, Update e Delete) para o gerenciamento de informações de alunos, utilizando o framework **FastAPI** integrado ao banco de dados **PostgreSQL** através do **SQLAlchemy**. O código foi desenvolvido em **Python**.

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
- [Endpoints Disponíveis](#endpoints-disponíveis)
- [Código](#código)
- [Teste](#testando-a-api)

### Pré-requisitos

- Ambiente Virtual ativado

```
 python -m venv venv*
 venv*\Scripts\activate
``` 
- Execução do aplicativo no ambiente virtual:
```
uvicorn main:app --reload
``` 
- Python
- PostgreSQL

### Instalação

```
pip install fastapi[all] python-dotenv sqlalchemy psycopg2
```

### Configuração do Banco de Dados

Criar um arquivo para o banco de dados [db.py](https://github.com/MeireMayumi/FastAPI-com-PostgreSQL/blob/main/db.py):

```ruby
#Importar os módulos de SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Módulo utilizado para carregar as variáveis de ambiente
from dotenv import load_dotenv
import os

#Carrega as variáveis do arquivo .env
load_dotenv()

#Recupera a URL do banco de dados da variável de ambiente
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

#Cria uma engine do  SQLAlchemy para se conectar ao banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Cria uma sessão que será usada para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base utilizada para as classes de modelo ORM
Base = declarative_base()
```

Para não expor os dados sensíveis no arquivo do banco de dados, será criado um arquivo `.env` com a URL de conexão do SQLAlchemy:

```
DATABASE_URL=postgresql://<usuario>:<senha>@<localhost>/<nome-do-banco>
```

### Endpoints disponíveis

A API inclui os seguintes endpoints para gerenciar registros de alunos:
<details>
<summary>Rota: POST/alunos/</summary>
  
  **Descrição**: Cria um novo aluno.

  **Entrada**: Objeto JSON contendo `nome` e `email`.
  
  **Resposta**: Objeto `Aluno` recém-criado.
</details>

<details>
<summary>Rota: GET/alunos/</summary>
  
  **Descrição**: Retorna uma lista com todos os alunos cadastrados.

  **Resposta**: Lista de objetos `Aluno`.
</details>
<details>
<summary>Rota: GET/alunos/{aluno_id}</summary>
  
  **Descrição**: Retorna os dados do aluno com base no id fornecido.

  
  **Resposta**: Objeto `Aluno`.
</details>
<details>
<summary>Rota: PUT/alunos/{aluno_id}</summary>
  
  **Descrição**: Atualiza os dados de um aluno existente.

  **Entrada**: Objeto JSON contendo os novos valores de `nome` e `email`
  
  **Resposta**: Objeto `Aluno` atualizado.
</details>

<details>
<summary>Rota: DELETE/alunos/{aluno_id}</summary>
  
  **Descrição**: Exclui um aluno com base no id fornecido.

  **Resposta**: Objeto `Aluno` excluído.
</details>

### Código
- Criar um arquivo [main.py](https://github.com/MeireMayumi/FastAPI-com-PostgreSQL/blob/main/main.py):
```ruby
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
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return Aluno.from_orm(aluno)

#Atualização de informações um aluno exustente
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

#Exclusão de um aluno baseado no id fornecido 
@app.delete("/alunos/{aluno_id}", response_model=Aluno)
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()
    return Aluno.from_orm(aluno)
```


### Testando a API

Swagger UI: http://127.0.0.1:8000/docs
