# Python 3.10 slim image kullan
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# Reports klasörü oluştur
RUN mkdir -p reports

# Port 8000'i aç
EXPOSE 8000

# Health check için curl kur
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Uygulamayı başlat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 