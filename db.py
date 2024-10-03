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