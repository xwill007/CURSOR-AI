@echo off
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo Error: No se pudo activar el entorno virtual.
    echo Creando nuevo entorno virtual...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

echo Instalando/Actualizando pip...
python -m pip install --upgrade pip

echo Instalando dependencias...
pip install -r requirements.txt
pip install python-multipart --no-cache-dir

echo Verificando instalación de módulos críticos...
python -c "import fastapi; import uvicorn; import python_multipart" 2>nul
if errorlevel 1 (
    echo Error: Algunas dependencias no se instalaron correctamente.
    echo Intentando reinstalar individualmente...
    pip install fastapi uvicorn python-multipart --no-cache-dir
)

echo Iniciando la API...
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo Desactivando entorno virtual...
cd ..
call deactivate 