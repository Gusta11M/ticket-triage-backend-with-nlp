FROM python:3.12-slim

# Evita pyc e buffering estranho
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências primeiro (melhor cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Arranque da API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]