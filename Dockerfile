# Usa una imagen base con Playwright y todas sus dependencias ya instaladas
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Establece el directorio de trabajo
WORKDIR /app

# Copia tu código y requerimientos
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala los navegadores necesarios (Chromium, Firefox, WebKit)
RUN playwright install

# Expón el puerto (Railway detecta esto)
EXPOSE 8000

# Comando para ejecutar tu app con Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
