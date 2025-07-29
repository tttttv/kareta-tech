FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY bot.py .
COPY main.py .
COPY .env .

ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]