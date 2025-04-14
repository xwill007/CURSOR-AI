from typing import Optional, List
import sqlite3
from pathlib import Path
from core.interfaces.lyrics_provider import LyricsProvider, LyricsData

class LocalDBProvider(LyricsProvider):
    """Implementación del proveedor de letras usando SQLite local."""

    def __init__(self, db_path: str = "lyrics.db"):
        """
        Inicializa la conexión a la base de datos.

        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.source = "local_db"
        self._init_db()

    def _init_db(self):
        """Inicializa la estructura de la base de datos si no existe."""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lyrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    artist TEXT NOT NULL,
                    title TEXT NOT NULL,
                    lyrics TEXT NOT NULL,
                    language TEXT DEFAULT 'en',
                    timestamps BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(artist, title)
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_artist_title ON lyrics(artist, title)")
            conn.commit()
        finally:
            conn.close()

    async def get_lyrics(self, artist: str, title: str) -> Optional[LyricsData]:
        """
        Obtiene letras de la base de datos local.

        Args:
            artist: Nombre del artista
            title: Título de la canción

        Returns:
            Optional[LyricsData]: Datos de la letra si se encuentra
        """
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT artist, title, lyrics, language, timestamps FROM lyrics WHERE artist = ? AND title = ?",
                (artist, title)
            )
            row = cursor.fetchone()
            
            if not row:
                return None

            return LyricsData(
                artist=row[0],
                title=row[1],
                lyrics=row[2],
                source=self.source,
                language=row[3],
                timestamps=bool(row[4])
            )
        finally:
            conn.close()

    async def search_lyrics(self, query: str) -> List[LyricsData]:
        """
        Busca letras en la base de datos local.

        Args:
            query: Texto a buscar

        Returns:
            List[LyricsData]: Lista de resultados
        """
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute(
                """
                SELECT artist, title, lyrics, language, timestamps 
                FROM lyrics 
                WHERE artist LIKE ? OR title LIKE ? OR lyrics LIKE ?
                LIMIT 10
                """,
                (f"%{query}%", f"%{query}%", f"%{query}%")
            )
            results = []
            for row in cursor:
                results.append(
                    LyricsData(
                        artist=row[0],
                        title=row[1],
                        lyrics=row[2],
                        source=self.source,
                        language=row[3],
                        timestamps=bool(row[4])
                    )
                )
            return results
        finally:
            conn.close()

    async def save_lyrics(self, lyrics_data: LyricsData) -> bool:
        """
        Guarda letras en la base de datos local.

        Args:
            lyrics_data: Datos de la letra a guardar

        Returns:
            bool: True si se guardó correctamente
        """
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                INSERT OR REPLACE INTO lyrics (artist, title, lyrics, language, timestamps)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    lyrics_data.artist,
                    lyrics_data.title,
                    lyrics_data.lyrics,
                    lyrics_data.language,
                    lyrics_data.timestamps
                )
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving to local DB: {e}")
            return False
        finally:
            conn.close()

    async def import_from_text(self, content: str, artist: str, title: str, language: str = "en") -> Optional[LyricsData]:
        """
        Imports lyrics from a text file content and saves it to the database.

        Args:
            content: Text content with timestamps
            artist: Artist name
            title: Song title
            language: Language code (default: "en")

        Returns:
            Optional[LyricsData]: Created lyrics data if successful, None if failed

        Example content format:
            [0:00] First line of lyrics
            [0:15] Second line of lyrics
            [0:30] Third line of lyrics
        """
        # Verify if content has timestamps
        if not any(line.strip().startswith("[") for line in content.splitlines()):
            return None

        lyrics_data = LyricsData(
            artist=artist,
            title=title,
            lyrics=content,
            source=self.source,
            language=language,
            timestamps=True
        )

        if await self.save_lyrics(lyrics_data):
            return lyrics_data
        return None 