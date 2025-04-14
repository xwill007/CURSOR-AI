from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from pathlib import Path
import shutil

from ..services.lyrics_service import LyricsService
from ..infrastructure.genius_provider import GeniusProvider
from ..infrastructure.local_db_provider import LocalDBProvider
from core.interfaces.lyrics_provider import LyricsData
from ..services.file_service import FileService

router = APIRouter(prefix="/lyrics", tags=["lyrics"])

# Asegurar que existe el directorio para guardar archivos
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class LyricsRequest(BaseModel):
    """Modelo para la solicitud de letras."""
    artist: str
    title: str

class LyricsResponse(BaseModel):
    """Modelo para la respuesta con letras."""
    title: str
    artist: str
    lyrics: str
    source: str
    language: str = "en"
    timestamps: bool = False

class UploadResponse(BaseModel):
    """Modelo de respuesta para la carga de archivos."""
    success: bool
    message: str
    details: Optional[str] = None
    file_path: Optional[str] = None
    content: Optional[str] = None

async def get_lyrics_service() -> LyricsService:
    """
    Dependencia para obtener el servicio de letras configurado.
    
    Returns:
        LyricsService: Servicio configurado con múltiples proveedores
    """
    # En producción, estas configuraciones vendrían de variables de entorno
    genius_provider = GeniusProvider(api_key="your_genius_api_key")
    local_provider = LocalDBProvider(db_path="lyrics.db")
    
    # El orden de los proveedores determina la prioridad de búsqueda
    return LyricsService([
        local_provider,  # Primero busca en la base local
        genius_provider  # Luego en Genius
    ])

@router.post("/", response_model=LyricsResponse)
async def get_lyrics(
    request: LyricsRequest,
    service: LyricsService = Depends(get_lyrics_service)
) -> LyricsResponse:
    """
    Obtiene las letras de una canción de cualquier proveedor disponible.
    
    Args:
        request: Datos de la solicitud
        service: Servicio de letras inyectado
        
    Returns:
        LyricsResponse: Datos de la letra encontrada
        
    Raises:
        HTTPException: Si no se encuentra la letra
    """
    if lyrics := await service.get_lyrics(request.artist, request.title):
        return LyricsResponse(**lyrics.dict())
    
    raise HTTPException(
        status_code=404,
        detail=f"No se encontró la letra para {request.title} de {request.artist}"
    )

@router.get("/search", response_model=List[LyricsResponse])
async def search_lyrics(
    query: str,
    service: LyricsService = Depends(get_lyrics_service)
) -> List[LyricsResponse]:
    """
    Busca letras en todos los proveedores disponibles.
    
    Args:
        query: Texto a buscar
        service: Servicio de letras inyectado
        
    Returns:
        List[LyricsResponse]: Lista de resultados encontrados
    """
    results = await service.search_lyrics(query)
    return [LyricsResponse(**result.dict()) for result in results]

@router.post("/upload")
async def upload_lyrics(
    file: UploadFile = File(...),
    artist: str = Form(...),
    title: str = Form(...),
    language: str = Form("en")
) -> JSONResponse:
    """
    Endpoint básico para probar la carga de archivos.
    """
    try:
        # Verificar extensión
        if not file.filename.endswith(('.txt', '.lrc')):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "Formato no válido",
                    "details": "Solo se permiten archivos .txt o .lrc"
                }
            )

        # Crear nombre de archivo seguro
        safe_filename = f"{artist}_{title}_{file.filename}"
        safe_filename = "".join(c for c in safe_filename if c.isalnum() or c in "._- ")
        file_path = UPLOAD_DIR / safe_filename

        # Guardar archivo
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Archivo subido correctamente",
                "details": {
                    "artist": artist,
                    "title": title,
                    "filename": safe_filename,
                    "language": language
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error al procesar el archivo",
                "details": str(e)
            }
        ) 