import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Usa el que te da Railway, o 8000 por defecto localmente
    uvicorn.run("app:app", host="0.0.0.0", port=port)
