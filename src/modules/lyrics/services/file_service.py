from typing import Optional, Tuple
import re
from datetime import datetime
from pathlib import Path

class FileService:
    """Servicio para manejar archivos de letras con marcas de tiempo."""

    @staticmethod
    def validate_timestamp_format(line: str) -> bool:
        """
        Valida si una línea tiene el formato correcto de marca de tiempo.
        Formato válido: [MM:SS] o [HH:MM:SS]
        """
        timestamp_pattern = r'^\[\d{1,2}:\d{2}(?::\d{2})?\]'
        return bool(re.match(timestamp_pattern, line.strip()))

    @staticmethod
    def parse_lyrics_file(content: str) -> Tuple[bool, str, Optional[str]]:
        """
        Analiza el contenido del archivo de letras.

        Args:
            content: Contenido del archivo

        Returns:
            Tuple[bool, str, Optional[str]]: 
                - bool: True si el archivo es válido
                - str: Contenido procesado o mensaje de error
                - Optional[str]: Detalles adicionales del error si existe
        """
        lines = content.splitlines()
        if not lines:
            return False, "El archivo está vacío", None

        # Verificar formato de marcas de tiempo
        valid_lines = []
        invalid_lines = []
        line_number = 0
        has_timestamps = False

        for line in lines:
            line_number += 1
            line = line.strip()
            
            # Saltar líneas vacías
            if not line:
                valid_lines.append(line)
                continue

            # Verificar si la línea tiene marca de tiempo
            if line.startswith('['):
                if FileService.validate_timestamp_format(line):
                    has_timestamps = True
                    valid_lines.append(line)
                else:
                    invalid_lines.append(f"Línea {line_number}: '{line}' - Formato de tiempo inválido")
            else:
                valid_lines.append(line)

        if not has_timestamps:
            return False, "No se encontraron marcas de tiempo válidas", None

        if invalid_lines:
            error_details = "\n".join(invalid_lines)
            return False, "El archivo contiene marcas de tiempo inválidas", error_details

        return True, "\n".join(valid_lines), None

    @staticmethod
    def save_lyrics_file(content: str, artist: str, title: str) -> Tuple[bool, str, Optional[str]]:
        """
        Guarda el contenido en un archivo local.

        Args:
            content: Contenido del archivo
            artist: Nombre del artista
            title: Título de la canción

        Returns:
            Tuple[bool, str, Optional[str]]:
                - bool: True si se guardó correctamente
                - str: Mensaje de éxito o error
                - Optional[str]: Ruta del archivo guardado o None
        """
        try:
            # Crear directorio lyrics si no existe
            lyrics_dir = Path("lyrics")
            lyrics_dir.mkdir(exist_ok=True)

            # Crear nombre de archivo seguro
            safe_name = f"{artist}_{title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            safe_name = "".join(c for c in safe_name if c.isalnum() or c in "._- ")
            
            file_path = lyrics_dir / safe_name
            
            # Guardar archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, "Archivo guardado correctamente", str(file_path)
        except Exception as e:
            return False, f"Error al guardar el archivo: {str(e)}", None 