# Comandos para el proyecto FastAPI

## Instalación inicial

### Instalar UV
```bash
pip install uv
```

### Crear un entorno virtual con UV
```bash
uv venv
```

### Activar el entorno virtual
#### En Windows (PowerShell)
```bash
# Es obligatorio cambiar la política de ejecución para activar entornos virtuales:
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Luego activa el entorno:
.venv\Scripts\activate
```

#### En Windows (CMD)
```bash
.venv\Scripts\activate.bat
```

#### En Linux/macOS
```bash
source .venv/bin/activate
```

### Verificar activación
Después de activar el entorno, deberías ver (nombre-entorno) al inicio del prompt:
```
(nombre-entorno) PS C:\ruta\al\proyecto>
```

### Instalar dependencias con UV
```bash
# Instalar todas las dependencias desde requirements.txt
uv pip install -r requirements.txt

# Asegúrate de que FastAPI está instalado
uv pip install fastapi

# Alternativa: instalar desde pyproject.toml
uv pip install -e .
```

## Ejecución del proyecto

### Ejecutar la aplicación
```bash
# Usando el punto de entrada en main.py (recomendado)
python main.py

# Alternativa: usando uvicorn directamente con alias (PowerShell)
# Primero crea un alias para uvicorn (solo necesitas hacerlo una vez por sesión):
Set-Alias -Name uvicorn -Value .venv\Scripts\uvicorn

# Luego puedes ejecutar:
uvicorn main:app --reload

# Alternativa: usando uvicorn con python -m
python -m uvicorn main:app --reload
```

## Desarrollo

### Formatear código con black
```bash
black .
```

### Ordenar imports con isort
```bash
isort .
```

### Verificar tipos con mypy
```bash
mypy .
```

## Acceso a la API

- API principal: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc

## Solución de problemas comunes

### Error de política de ejecución en PowerShell

Si recibes un error como:
```
... no se puede cargar el archivo ... porque la ejecución de scripts está deshabilitada en este sistema.
```

Ejecuta el siguiente comando para permitir la ejecución de scripts en la sesión actual:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

Luego intenta activar el entorno virtual nuevamente.

### Módulos no encontrados

Si recibes errores como "ModuleNotFoundError: No module named 'fastapi'", verifica:

1. Que el entorno virtual esté correctamente activado (deberías ver el prefijo con el nombre)
2. Reinstala las dependencias dentro del entorno activado:
```bash
uv pip install -r requirements.txt
uv pip install fastapi
```

### Error con uvicorn

Si recibes un error como "El término 'uvicorn' no se reconoce":

1. Asegúrate de que estás usando el entorno virtual activado
2. **Solución recomendada**: Crea un alias en PowerShell:
```bash
Set-Alias -Name uvicorn -Value .venv\Scripts\uvicorn
```
3. Usa la versión de módulo Python:
```bash
python -m uvicorn main:app --reload
```
4. O ejecuta directamente el script principal:
```bash
python main.py
```

### Desactivar entorno virtual

Cuando termines de trabajar, puedes desactivar el entorno virtual:
```bash
deactivate
``` 