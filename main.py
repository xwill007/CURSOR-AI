from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import lyricsgenius
import os
from googletrans import Translator

# Cargar variables de entorno
load_dotenv()

# Inicializar FastAPI
app = FastAPI(
    title="API de Traducción de Letras",
    description="API para obtener y traducir letras de canciones usando Genius y Google Translate",
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

# Inicializar Genius API
genius = lyricsgenius.Genius(os.getenv("GENIUS_API_KEY"))
translator = Translator()

class SongRequest(BaseModel):
    artist: str
    title: str
    target_lang: str = "es"  # Idioma destino por defecto: español

@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a la API de Traducción de Letras!"}

@app.post("/translate-lyrics")
async def translate_lyrics(song_request: SongRequest):
    try:
        # Buscar la canción
        song = genius.search_song(song_request.title, song_request.artist)
        if not song:
            raise HTTPException(status_code=404, detail="Canción no encontrada")
        
        # Traducir letras
        translated_lyrics = translator.translate(
            song.lyrics,
            dest=song_request.target_lang
        )
        
        return {
            "original_lyrics": song.lyrics,
            "translated_lyrics": translated_lyrics.text,
            "song_title": song.title,
            "artist": song.artist,
            "target_language": song_request.target_lang
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 