from abc import ABC, abstractmethod
from typing import Optional, Protocol

from pydantic import BaseModel

class LyricsData(BaseModel):
    """Modelo de datos para las letras de canciones."""
    title: str
    artist: str
    lyrics: str
    source: str
    language: str = "en"
    timestamps: bool = False

class LyricsProvider(Protocol):
    """Protocolo base para proveedores de letras de canciones."""
    
    @abstractmethod
    async def get_lyrics(self, artist: str, title: str) -> Optional[LyricsData]:
        """
        Obtiene las letras de una canción.

        Args:
            artist: Nombre del artista
            title: Título de la canción

        Returns:
            Optional[LyricsData]: Datos de la letra si se encuentra, None si no
        """
        pass

    @abstractmethod
    async def search_lyrics(self, query: str) -> list[LyricsData]:
        """
        Busca letras de canciones por texto.

        Args:
            query: Texto a buscar

        Returns:
            list[LyricsData]: Lista de resultados encontrados
        """
        pass 