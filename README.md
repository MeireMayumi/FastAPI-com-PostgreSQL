# FastAPI com PostgreSQL no Docker

Esta API permite a execução das quatro operações básicas **CRUD** (Create, Read, Update e Delete) para o gerenciamento de informações de alunos, utilizando o framework **FastAPI** integrado ao banco de dados **PostgreSQL** através do **SQLAlchemy**. O código foi desenvolvido em **Python** e a aplicação foi containerizada pelo **Docker**.

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
- [Endpoints Disponíveis](#endpoints-disponíveis)
- [Código](#código)
- [Docker](#docker)
- [Teste](#testando-a-api)

### Pré-requisitos

- Python
- PostgreSQL
- Rancher Desktop

### Configuração do Banco de Dados

Crie um arquivo [db.py](https://github.com/MeireMayumi/FastAPI-com-PostgreSQL/blob/main/db.py) que define a conexão com o banco de dados, a criação da sessão e a base para os modelos ORM.

Para não expor os dados sensíveis no arquivo do banco de dados e no docker-compose, crie o arquivo [.env](https://github.com/MeireMayumi/FastAPI-com-PostgreSQL/blob/main/.env).

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

Crie um arquivo [main.py](https://github.com/MeireMayumi/FastAPI-com-PostgreSQL/blob/main/main.py) que contém o código para implementar a aplicação FastAPI, que gerencia as operações CRUD para o gerenciamento de alunos. 


### Docker

Para automatizar o processo de construção e execução da imagem do contêiner, crie o arquivo [Dockerfile](https://github.com/MeireMayumi/FastAPI-com-PostgreSQL/blob/main/Dockerfile), que contém as instruções necessárias para configurar o ambiente, instalar as dependências e construir a imagem.

Para simplificar a execução de múltiplos contêineres com um único comando, crie o arquivo [compose.yaml](https://github.com/MeireMayumi/FastAPI-com-PostgreSQL/blob/main/compose.yaml), que permite definir e configurar serviços, redes e volumes.

Para facilitar o gerenciamento das dependências do projeto, crie o arquivo [requirements.txt](https://github.com/MeireMayumi/FastAPI-com-PostgreSQL/blob/main/requirements.txt), que lista todas as bibliotecas e suas versões necessárias.

Para garantir que a aplicação inicie somente depois que o banco de dados estiver pronto, foi criado o arquivo [wait-for-it.sh](https://github.com/MeireMayumi/FastAPI-com-PostgreSQL/blob/main/wait-for-it.sh).

Para criar e inicializar os contêineres, certifique-se de estar no diretório raiz em que o arquivo compose.yaml se encontra e executar o seguinte comando:
```
docker-compose up
```

Para rodar o contêiner em segundo plano, sem bloquear o terminal que iniciou a execução:
```
docker-compose up -d
```

### Testando a API

Swagger UI: http://localhost:8000/docs

pgAdmin4: http://localhost:8080
