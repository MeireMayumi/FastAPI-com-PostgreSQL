FROM python:3.12

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . . 

CMD ["./wait-for-it.sh", "db", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
