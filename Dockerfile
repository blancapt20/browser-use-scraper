# Python 3.11 base
FROM python:3.11-slim

# Instalar dependencias del sistema para Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libxkbcommon0 \
    libasound2 libatspi2.0-0 libx11-6 libdbus-1-3 wget unzip \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app
COPY . .

# Instalar pip y dependencias Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Instalar playwright y navegadores
RUN pip install playwright
RUN playwright install

# Exponer puerto y lanzar app
EXPOSE 8000
                                                                                                                                                                                                CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "start.py"]
