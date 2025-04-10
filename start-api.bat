@echo off
echo Iniciando la API de FastAPI...
echo.

rem Activar el entorno virtual
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo Error: No se pudo activar el entorno virtual.
    echo Asegurate de que el entorno virtual exista en .venv\Scripts\activate.bat
    exit /b 1
)

echo Entorno virtual activado correctamente.
echo.

rem Ejecutar la aplicación
echo Iniciando la aplicación FastAPI...
echo Presiona Ctrl+C para detener el servidor.
echo.

python main.py

rem Si llegamos aquí, es porque la aplicación terminó
call deactivate
echo.
echo Aplicación finalizada y entorno virtual desactivado.
pause 