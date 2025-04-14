from typing import Optional, List
import lyricsgenius
from core.interfaces.lyrics_provider import LyricsProvider, LyricsData

class GeniusProvider(LyricsProvider):
    """Implementación del proveedor de letras usando Genius API."""

    def __init__(self, api_key: str):
        """
        Inicializa el cliente de Genius.

        Args:
            api_key: API key de Genius
        """
        self.genius = lyricsgenius.Genius(api_key)
        self.genius.verbose = False
        self.source = "genius"

    async def get_lyrics(self, artist: str, title: str) -> Optional[LyricsData]:
        """
        Obtiene letras de Genius API.

        Args:
            artist: Nombre del artista
            title: Título de la canción

        Returns:
            Optional[LyricsData]: Datos de la letra si se encuentra
        """
        try:
            song = self.genius.search_song(title, artist)
            if not song:
                return None

            return LyricsData(
                title=song.title,
                artist=song.artist,
                lyrics=song.lyrics,
                source=self.source,
                timestamps=False
            )
        except Exception as e:
            print(f"Error fetching from Genius: {e}")
            return None

    async def search_lyrics(self, query: str) -> List[LyricsData]:
        """
        Busca letras en Genius.

        Args:
            query: Texto a buscar

        Returns:
            List[LyricsData]: Lista de resultados
        """
        try:
            songs = self.genius.search_songs(query)
            results = []
            
            for song in songs['hits']:
                results.append(
                    LyricsData(
                        title=song['result']['title'],
                        artist=song['result']['primary_artist']['name'],
                        lyrics=song['result'].get('lyrics', ''),
                        source=self.source,
                        timestamps=False
                    )
                )
            return results
        except Exception as e:
            print(f"Error searching in Genius: {e}")
            return [] 