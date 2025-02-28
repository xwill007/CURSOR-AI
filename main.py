from fastapi import FastAPI, HTTPException, status, Depends, Query, Body, Path
from fastapi.middleware.cors import CORSMiddleware
from settings import settings
from schemas import Plato
from typing import List, Dict, Optional, Annotated

# Create the FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated database for dishes
platos_db: Dict[int, Plato] = {
    1: Plato(id=1, name="Paella", precio=15.50),
    2: Plato(id=2, name="Tortilla Española", precio=8.75),
    3: Plato(id=3, name="Gazpacho", precio=6.25),
}

# Example routes
@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: A welcome message
    """
    return {"message": "Welcome to my FastAPI API!"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status information
    """
    return {"status": "ok"}

# Example route for items
@app.get("/items/")
async def read_items():
    """
    Get a list of example items.
    
    Returns:
        dict: A dictionary of example items
    """
    fake_items_db = {"item1": {"name": "Foo"}, "item2": {"name": "Bar"}}
    return fake_items_db

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    """
    Get a specific item by ID.
    
    Args:
        item_id (str): The ID of the item to retrieve
        
    Returns:
        dict: The item data
        
    Raises:
        HTTPException: If the item is not found
    """
    fake_items_db = {"item1": {"name": "Foo"}, "item2": {"name": "Bar"}}
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]

# CRUD for the Plato model

# Create - Create a new dish
@app.post("/platos/", response_model=Plato, status_code=status.HTTP_201_CREATED)
async def create_plato(plato: Annotated[Plato, Body(description="Data for the new dish")]):
    """
    Creates a new dish in the database.
    
    - **id**: Unique identifier for the dish
    - **name**: Name of the dish
    - **precio**: Price of the dish
    """
    if plato.id in platos_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A dish with ID {plato.id} already exists"
        )
    platos_db[plato.id] = plato
    return plato

# Read - Get all dishes with pagination
@app.get("/platos/", response_model=List[Plato])
async def read_platos(
    skip: Annotated[int, Query(description="Number of records to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Maximum number of records to return", ge=1, le=100)] = 10
):
    """
    Gets a list of dishes with pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    return list(platos_db.values())[skip:skip + limit]

# Read - Get a specific dish by ID
@app.get("/platos/{plato_id}", response_model=Plato)
async def read_plato(
    plato_id: Annotated[int, Path(description="ID of the dish to retrieve", ge=1)]
):
    """
    Gets a specific dish by its ID.
    
    - **plato_id**: ID of the dish to retrieve
    """
    if plato_id not in platos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No dish found with ID {plato_id}"
        )
    return platos_db[plato_id]

# Update - Update an existing dish
@app.put("/platos/{plato_id}", response_model=Plato)
async def update_plato(
    plato_id: Annotated[int, Path(description="ID of the dish to update", ge=1)],
    plato: Annotated[Plato, Body(description="Updated dish data")]
):
    """
    Updates an existing dish.
    
    - **plato_id**: ID of the dish to update
    - **plato**: Updated dish data
    """
    if plato_id not in platos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No dish found with ID {plato_id}"
        )
    
    # Ensure the ID in the path matches the ID in the body
    if plato_id != plato.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The ID in the URL ({plato_id}) does not match the ID in the request body ({plato.id})"
        )
    
    platos_db[plato_id] = plato
    return plato

# Update - Partially update a dish (PATCH)
@app.patch("/platos/{plato_id}", response_model=Plato)
async def patch_plato(
    plato_id: Annotated[int, Path(description="ID of the dish to partially update", ge=1)],
    name: Annotated[Optional[str], Body(description="New dish name")] = None,
    precio: Annotated[Optional[float], Body(description="New dish price")] = None
):
    """
    Partially updates an existing dish.
    
    - **plato_id**: ID of the dish to partially update
    - **name**: New dish name (optional)
    - **precio**: New dish price (optional)
    """
    if plato_id not in platos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No dish found with ID {plato_id}"
        )
    
    plato_actual = platos_db[plato_id]
    plato_data = plato_actual.model_dump()
    
    # Update only the provided fields
    if name is not None:
        plato_data["name"] = name
    if precio is not None:
        plato_data["precio"] = precio
    
    plato_actualizado = Plato(**plato_data)
    platos_db[plato_id] = plato_actualizado
    return plato_actualizado

# Delete - Delete a dish
@app.delete("/platos/{plato_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plato(
    plato_id: Annotated[int, Path(description="ID of the dish to delete", ge=1)]
):
    """
    Deletes a dish from the database.
    
    - **plato_id**: ID of the dish to delete
    """
    if plato_id not in platos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No dish found with ID {plato_id}"
        )
    
    del platos_db[plato_id]
    return None

# Run the application if called directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.RELOAD
    )
