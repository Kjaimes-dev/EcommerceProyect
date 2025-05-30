# app/api/schemas/sproduct.py
from pydantic import BaseModel, constr, condecimal, conint, field_validator
from enum import Enum
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CategoriaProducto(str, Enum):
    ropa = 'ropa'
    collares = 'collares'

class ProductoBaseSchema(BaseModel):
    nombre: constr(min_length=1, max_length=100)
    descripcion: Optional[str] = None
    precio: condecimal(gt=0, max_digits=10, decimal_places=2)
    stock: conint(ge=0)
    categoria: CategoriaProducto

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v):
        if not v or not v.strip():
            logger.warning("[ProductoBaseSchema] nombre está vacío o nulo")
        return v

    @field_validator('precio')
    @classmethod
    def validar_precio(cls, v):
        if v is None or v <= 0:
            logger.warning(f"[ProductoBaseSchema] precio inválido: {v}")
        return v

    @field_validator('stock')
    @classmethod
    def validar_stock(cls, v):
        if v is None or v < 0:
            logger.warning(f"[ProductoBaseSchema] stock inválido: {v}")
        return v

    @field_validator('categoria')
    @classmethod
    def validar_categoria(cls, v):
        try:
            if isinstance(v, str):
                v = CategoriaProducto(v)
            if v not in CategoriaProducto:
                logger.warning(f"[ProductoBaseSchema] categoria inválida: {v}")
        except ValueError:
            logger.warning(f"[ProductoBaseSchema] categoria no válida: {v}")
        return v

class ProductoCreateUpdateSchema(ProductoBaseSchema):
    pass

class ProductoSchema(ProductoBaseSchema):
    id_producto: int

    @field_validator('id_producto')
    @classmethod
    def validar_id_producto(cls, v):
        if v <= 0:
            logger.warning("[ProductoSchema] id_producto debe ser mayor que cero")
        return v

    class Config:
        from_attributes = True
