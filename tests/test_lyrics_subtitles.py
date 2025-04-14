import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app

client = TestClient(app)

@pytest.fixture
def mock_genius():
    """
    Creates a mock for the Genius API client.
    
    Returns:
        Mock: A configured mock object for testing.
    """
    mock_song = Mock()
    mock_song.lyrics = """[Verse 1]
Yesterday, all my troubles seemed so far away
[0:15]Now it looks as though they're here to stay
[0:30]Oh, I believe in yesterday

[Chorus]
[0:45]Suddenly, I'm not half the man I used to be
[1:00]There's a shadow hanging over me
[1:15]Oh, yesterday came suddenly"""
    mock_song.title = "Yesterday"
    mock_song.artist = "The Beatles"
    
    with patch('lyricsgenius.Genius') as mock_genius:
        mock_genius.return_value.search_song.return_value = mock_song
        yield mock_genius

@pytest.fixture
def mock_translator():
    """
    Creates a mock for the Google Translator.
    
    Returns:
        Mock: A configured mock object for testing.
    """
    with patch('googletrans.Translator') as mock_translator:
        mock_translation = Mock()
        mock_translation.text = """[Verso 1]
Ayer, todos mis problemas parecían tan lejanos
[0:15]Ahora parece que están aquí para quedarse
[0:30]Oh, creo en el ayer

[Coro]
[0:45]De repente, no soy ni la mitad del hombre que solía ser
[1:00]Hay una sombra sobre mí
[1:15]Oh, el ayer llegó de repente"""
        mock_translator.return_value.translate.return_value = mock_translation
        yield mock_translator

@pytest.mark.asyncio
async def test_get_lyrics_with_subtitles_success(mock_genius, mock_translator):
    """
    Tests successful retrieval and translation of lyrics with timestamps.
    
    Args:
        mock_genius: Mock object for Genius API
        mock_translator: Mock object for Google Translator
    """
    response = client.post(
        "/lyrics-subtitles",
        json={
            "artist": "The Beatles",
            "title": "Yesterday",
            "target_lang": "es"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "original_lyrics" in data
    assert "translated_lyrics" in data
    assert "[0:15]" in data["original_lyrics"]
    assert "[0:15]" in data["translated_lyrics"]
    assert data["song_title"] == "Yesterday"
    assert data["artist"] == "The Beatles"

@pytest.mark.asyncio
async def test_get_lyrics_song_not_found(mock_genius):
    """
    Tests the error handling when a song is not found.
    
    Args:
        mock_genius: Mock object for Genius API
    """
    mock_genius.return_value.search_song.return_value = None
    
    response = client.post(
        "/lyrics-subtitles",
        json={
            "artist": "Nonexistent Artist",
            "title": "Nonexistent Song",
            "target_lang": "es"
        }
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Canción no encontrada"

@pytest.mark.asyncio
async def test_get_lyrics_invalid_language(mock_genius, mock_translator):
    """
    Tests the error handling when an invalid target language is provided.
    
    Args:
        mock_genius: Mock object for Genius API
        mock_translator: Mock object for Google Translator
    """
    mock_translator.return_value.translate.side_effect = ValueError("Invalid language code")
    
    response = client.post(
        "/lyrics-subtitles",
        json={
            "artist": "The Beatles",
            "title": "Yesterday",
            "target_lang": "invalid_lang"
        }
    )
    
    assert response.status_code == 400
    assert "Código de idioma inválido" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_lyrics_with_missing_timestamps():
    """
    Tests the error handling when lyrics don't contain proper timestamp formatting.
    """
    with patch('lyricsgenius.Genius') as mock_genius:
        mock_song = Mock()
        mock_song.lyrics = "Lyrics without any timestamps"
        mock_genius.return_value.search_song.return_value = mock_song
        
        response = client.post(
            "/lyrics-subtitles",
            json={
                "artist": "The Beatles",
                "title": "Yesterday",
                "target_lang": "es"
            }
        )
        
        assert response.status_code == 422
        assert "No se encontraron marcas de tiempo" in response.json()["detail"] 