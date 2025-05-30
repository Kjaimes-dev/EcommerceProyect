# app/api/schemas/scliente.py

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# para crear o actualizar cliente (input)
class ClienteCreateUpdateSchema(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str
    cedula: str
    direccion: str

    @field_validator('nombre', 'telefono', 'cedula', 'direccion')
    @classmethod
    def validate_non_empty(cls, v, info):
        if not v or not v.strip():
            logger.warning(f"[ClienteCreateUpdateSchema] Campo vacío o nulo: {info.field_name}")
        return v

# para mostrar cliente (output)
class ClienteSchema(ClienteCreateUpdateSchema):
    id_cliente: int

    @field_validator('id_cliente')
    @classmethod
    def validate_id_cliente(cls, v):
        if v <= 0:
            logger.warning("[ClienteSchema] id_cliente debe ser mayor que cero")
        return v

    class Config:
        from_attributes = True
