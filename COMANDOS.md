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
```bash
# En Windows (CMD)
.venv\Scripts\activate.bat

# En Linux/macOS
source .venv/bin/activate
```

### Verificar activación
Después de activar el entorno, deberías ver (venv) al inicio del prompt:
```
(.venv) C:\ruta\al\proyecto>
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

## ⚠️ EJECUCION DEL PROYECTO ⚠️

### Iniciar la API (método recomendado)

Para iniciar la API de forma sencilla, usa el archivo batch:

```Comando cmd```
start-api.bat
`````````````````

Este archivo batch:
1. Activa el entorno virtual automáticamente
2. Ejecuta la aplicación FastAPI
3. Desactiva el entorno virtual al finalizar

### Ejecutar manualmente la aplicación
```bash
# Paso 1: Activar el entorno virtual
.venv\Scripts\activate.bat

# Paso 2: Ejecutar la aplicación con Python
python main.py

# O con uvicorn directamente:
.venv\Scripts\uvicorn main:app --reload
```

## Peticiones a la API

### En CMD con curl (Windows)
Si prefieres usar curl genuino, puedes descargarlo desde https://curl.se/windows/ o usar:

```cmd
# Petición GET a la ruta principal
curl -s http://localhost:8000/

# Obtener lista de items
curl -s http://localhost:8000/items

# Obtener un item específico por ID
curl -s http://localhost:8000/items/1

# Crear un nuevo item (POST)
curl -s -X POST -H "Content-Type: application/json" -d "{\"nombre\":\"Nuevo Item\",\"precio\":29.99,\"disponible\":true}" http://localhost:8000/items

# Actualizar un item (PUT)
curl -s -X PUT -H "Content-Type: application/json" -d "{\"nombre\":\"Item Actualizado\",\"precio\":39.99,\"disponible\":true}" http://localhost:8000/items/1

# Eliminar un item (DELETE)
curl -s -X DELETE http://localhost:8000/items/1
```

### En Linux/Mac con curl
```bash
# Petición GET a la ruta principal
curl -s http://localhost:8000/

# Obtener lista de items
curl -s http://localhost:8000/items

# Obtener un item específico por ID
curl -s http://localhost:8000/items/1

# Crear un nuevo item (POST)
curl -s -X POST -H "Content-Type: application/json" -d '{"nombre":"Nuevo Item","precio":29.99,"disponible":true}' http://localhost:8000/items

# Actualizar un item (PUT)
curl -s -X PUT -H "Content-Type: application/json" -d '{"nombre":"Item Actualizado","precio":39.99,"disponible":true}' http://localhost:8000/items/1

# Eliminar un item (DELETE)
curl -s -X DELETE http://localhost:8000/items/1
```

### Usando un navegador
Para rutas GET simples, puedes usar directamente un navegador:
- Ruta principal: http://localhost:8000/
- Documentación Swagger: http://localhost:8000/docs (recomendado para probar la API)
- Lista de items: http://localhost:8000/items

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

## Control de versiones con Git y GitHub

### Inicializar un repositorio Git (si aún no existe)
```bash
git init
```

### Configurar usuario Git (si es la primera vez)
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

### Verificar configuración de Git y GitHub

```bash
# Ver toda la configuración de Git
git config --list

# Ver configuración específica de usuario
git config user.name
git config user.email

# Verificar conexión con remoto (GitHub)
git remote -v

# Verificar el estado actual del repositorio
git status

# Verificar ramas y su estado
git branch -vv

# Verificar si tienes acceso a GitHub (requiere GitHub CLI)
gh auth status
```

### Usando el paginador en Git (less)

Muchos comandos de Git como `git log` o `git config --list` muestran sus resultados usando un paginador (generalmente `less`). Cuando veas `:` al final de la salida, significa que estás en el modo paginador.

```
Comandos básicos del paginador:
- q - Salir del paginador y volver al prompt
- Flechas arriba/abajo - Desplazarse línea por línea
- Barra espaciadora - Avanzar una página completa
- b - Retroceder una página
- /palabra - Buscar "palabra" en el texto
- n - Ir a la siguiente ocurrencia de la búsqueda
- N - Ir a la ocurrencia anterior de la búsqueda
- g - Ir al inicio del texto
- G - Ir al final del texto
```

### Añadir todos los archivos al staging
```bash
git add .
```

### Crear el primer commit
```bash
git commit -m "Commit inicial: Esqueleto del proyecto FastAPI"
```

### Conectar con GitHub

1. Primero, crea un nuevo repositorio en GitHub
   - Ve a https://github.com/new
   - Asigna un nombre al repositorio (ej. "fastapi-app")
   - No inicialices el repositorio con README, .gitignore o licencia
   - Haz clic en "Crear repositorio"

2. Conecta tu repositorio local con GitHub:
```bash
# Si es la primera vez que conectas este repositorio
git remote add origin https://github.com/tu-usuario/nombre-del-repo.git

# Si recibes el error "remote origin already exists", tienes dos opciones:

# Opción 1: Ver la URL actual del remoto
git remote -v

# Opción 2: Eliminar el remoto existente y añadir el nuevo
git remote remove origin
git remote add origin https://github.com/tu-usuario/nombre-del-repo.git

# Opción 3: Actualizar la URL del remoto existente
git remote set-url origin https://github.com/tu-usuario/nombre-del-repo.git
```

3. Sube tus cambios a GitHub:
```bash
git push -u origin main

# Si el push falla con "rejected", puede que necesites forzar el push
# (¡PRECAUCIÓN! Esto sobrescribirá lo que exista en el repositorio remoto)
git push -u origin main --force
```

### Comandos Git comunes

```bash
# Ver el estado actual
git status

# Ver commits realizados
git log --oneline

# Crear una nueva rama
git checkout -b nombre-rama

# Cambiar de rama
git checkout nombre-rama

# Traer cambios de GitHub
git pull

# Subir cambios a GitHub
git push
```

## Acceso a la API

- API principal: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs
- Documentación ReDoc: http://localhost:8000/redoc

## Solución de problemas comunes

### Módulos no encontrados

Si recibes errores como "ModuleNotFoundError: No module named 'fastapi'", verifica:

1. Que el entorno virtual esté correctamente activado (deberías ver el prefijo con el nombre)
2. Reinstala las dependencias dentro del entorno activado:
```bash
uv pip install -r requirements.txt
uv pip install fastapi
```

## ⚠️ DESACTIVAR ENTORNO VIRTUAL ⚠️

Tienes dos opciones para desactivar el entorno virtual:

1. Si estás ejecutando la aplicación, presiona `Ctrl+C` para detenerla. El script batch automáticamente desactivará el entorno virtual.

2. Si has activado el entorno manualmente, usa:
```bash
deactivate
``` 