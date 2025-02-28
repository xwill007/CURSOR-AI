from pydantic import BaseModel
from typing import Optional

class Plato(BaseModel):
    """
    Model representing a food dish.
    
    Attributes:
        id: Unique identifier for the dish
        name: Name of the dish
        precio: Price of the dish
    """
    id: int
    name: str
    precio: float
    
    class Config:
        """Configuration for the Pydantic model"""
        from_attributes = True  # For ORM compatibility
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Paella",
                "precio": 15.50
            }
        } 