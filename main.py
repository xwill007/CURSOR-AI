from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from settings import settings

# Inicializar la aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos
class Item(BaseModel):
    id: Optional[int] = None
    nombre: str
    precio: float
    disponible: bool = True

# Almacenamiento de datos en memoria
items_db = {}
contador_id = 1

# Rutas API
@app.get("/")
async def raiz():
    """
    Endpoint principal que retorna un mensaje de bienvenida.
    
    Returns:
        dict: Mensaje de bienvenida
    """
    return {"mensaje": "Bienvenido a mi API con FastAPI"}

@app.get("/items", response_model=List[Item])
async def obtener_items():
    """
    Obtiene todos los items.
    
    Returns:
        List[Item]: Lista de todos los items
    """
    return list(items_db.values())

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def crear_item(item: Item):
    """
    Crea un nuevo item.
    
    Args:
        item: Datos del item a crear
        
    Returns:
        Item: Item creado con su ID asignado
    """
    global contador_id
    nuevo_item = item.model_copy(update={"id": contador_id})
    items_db[contador_id] = nuevo_item
    contador_id += 1
    return nuevo_item

@app.get("/items/{item_id}", response_model=Item)
async def obtener_item(item_id: int):
    """
    Obtiene un item específico por su ID.
    
    Args:
        item_id: ID del item a obtener
        
    Returns:
        Item: Item encontrado
        
    Raises:
        HTTPException: Si el item no existe
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def actualizar_item(item_id: int, item: Item):
    """
    Actualiza un item existente.
    
    Args:
        item_id: ID del item a actualizar
        item: Nuevos datos del item
        
    Returns:
        Item: Item actualizado
        
    Raises:
        HTTPException: Si el item no existe
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    
    items_db[item_id] = item.model_copy(update={"id": item_id})
    return items_db[item_id]

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_item(item_id: int):
    """
    Elimina un item.
    
    Args:
        item_id: ID del item a eliminar
        
    Raises:
        HTTPException: Si el item no existe
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    
    del items_db[item_id]

# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.RELOAD
    ) 