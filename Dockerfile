FROM python:3.11-slim

WORKDIR /app

# Dépendances système pour lxml
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 libxslt1.1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Créer le répertoire de données persistant
RUN mkdir -p /app/data

EXPOSE 5000

ENV FLASK_APP=app
ENV FLASK_ENV=production

CMD ["python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]
