from typing import List, Optional
from core.interfaces.lyrics_provider import LyricsData, LyricsProvider

class LyricsService:
    """
    Servicio principal para obtener letras de canciones.
    Implementa el patrón Strategy para usar múltiples proveedores.
    """

    def __init__(self, providers: List[LyricsProvider]):
        """
        Inicializa el servicio con una lista de proveedores.

        Args:
            providers: Lista de proveedores de letras
        """
        self.providers = providers

    async def get_lyrics(self, artist: str, title: str) -> Optional[LyricsData]:
        """
        Busca letras en todos los proveedores disponibles.

        Args:
            artist: Nombre del artista
            title: Título de la canción

        Returns:
            Optional[LyricsData]: Primera letra encontrada o None si no se encuentra
        """
        for provider in self.providers:
            try:
                if lyrics := await provider.get_lyrics(artist, title):
                    return lyrics
            except Exception as e:
                # Log error but continue with next provider
                print(f"Error with provider {provider.__class__.__name__}: {e}")
                continue
        return None

    async def search_lyrics(self, query: str) -> List[LyricsData]:
        """
        Busca letras en todos los proveedores.

        Args:
            query: Texto a buscar

        Returns:
            List[LyricsData]: Lista combinada de resultados de todos los proveedores
        """
        results = []
        for provider in self.providers:
            try:
                provider_results = await provider.search_lyrics(query)
                results.extend(provider_results)
            except Exception as e:
                # Log error but continue with next provider
                print(f"Error with provider {provider.__class__.__name__}: {e}")
                continue
        return results 