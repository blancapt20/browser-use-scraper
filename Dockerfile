FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . .

# Actualizar pip por si acaso
RUN python -m pip install --upgrade pip

# Instalar dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Instalar navegadores (opcional, por si no está ya)
RUN playwright install

# Exponer puerto
EXPOSE 8000

# Comando para correr la app FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
