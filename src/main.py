from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Crear la aplicación FastAPI
app = FastAPI(
    title="Lyrics API",
    description="API para gestionar letras de canciones con marcas de tiempo",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de prueba
@app.get("/")
async def root():
    return {"message": "API de letras funcionando correctamente"}

# Importar rutas de los módulos
try:
    from modules.lyrics.api.routes import router as lyrics_router
    app.include_router(lyrics_router)
except ImportError as e:
    print(f"Advertencia: No se pudo cargar el módulo de letras: {e}")
    print("La API funcionará con funcionalidad limitada.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 