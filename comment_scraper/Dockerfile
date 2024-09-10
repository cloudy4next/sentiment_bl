FROM python:3.9-slim

WORKDIR /app

COPY main.py ./
COPY process_comments.py ./
COPY requirements.txt ./
COPY .env ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
